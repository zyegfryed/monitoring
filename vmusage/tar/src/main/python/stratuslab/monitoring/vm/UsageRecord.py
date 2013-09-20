#
# Copyright (c) 2013, Centre National de la Recherche Scientifique (CNRS)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import libvirt
import xml.etree.ElementTree as ET

VM_STATES = {
    0: 'undefined',
    1: 'running',
    2: 'blocked',
    3: 'paused',
    4: 'shutdown',
    5: 'shutoff',
    6: 'crashed',
    7: 'pmsuspended',
    8: 'last',
}


class UsageRecord(object):

    def __init__(self, libvirt_url):
        self.connection = libvirt.open(libvirt_url)

    @staticmethod
    def _dom_network_io(dom, interfaces):
        """
        Provides the total received (net_rx) and transmitted (net_tx)
        bytes for all of the domain's network interfaces.  Return value
        is a dict with this information.
        """
        rx_total = 0L
        tx_total = 0L
        for interface in interfaces:
            (rx, _, _, _, tx, _, _, _) =  dom.interfaceStats(interface)
            rx_total += rx
            tx_total += tx
        return {'net_rx': rx_total, 'net_tx': tx_total}

    @staticmethod
    def _dom_disk_io(dom, disks):
        """
        Provides the total read (disk_read) and written (disk_written)
        bytes for all of the domain's disks.  Return value is a dict
        with this information.
        """
        rbytes_total = 0L
        wbytes_total = 0L
        for disk in disks:
            (_, rbytes, _, wbytes, _) =  dom.blockStats(disk)
            rbytes_total += rbytes
            wbytes_total += wbytes
        return {'disk_read': rbytes_total, 'disk_written': wbytes_total}

    @staticmethod
    def _dom_state_cpu_memory(dom):
        """
        Provides statistics about the given domain as a dict.  The
        values are 'state' (as defined by libvirt), 'memory' (in bytes),
        'vcpu', and 'cpu_time' (in seconds).
        """
        (state, maxMem_kb, memory_kb, vcpu, cpu_time_ns) = dom.info()
        return {
            'state': VM_STATES[state],
            'memory' : memory_kb * 1000L,
            'vcpu': vcpu,
            'cpu_time': cpu_time_ns/1000000000L
        }

    @staticmethod
    def _dom_xml_info(dom):
        """
        Returns a tuple with the following values: 1) a dict with 'name'
        and 'uuid' defined, 2) a list of disk devices, and 3) a list of
        network interfaces.  This information is gathered from the domain's
        XML description.
        """
        domxml = dom.XMLDesc(0)

        root = ET.fromstring(domxml)

        name = root.find('name').text
        uuid = root.find('uuid').text

        disks = []
        for disk in root.findall('./devices/disk/target'):
            dev = disk.get('dev')
            if dev:
                disks.append(dev)

        interfaces = []
        for interface in root.findall('./devices/interface/target'):
            dev = interface.get('dev')
            if dev:
                interfaces.append(dev)

        return ({'name': name, 'uuid': uuid}, disks, interfaces)

    @staticmethod
    def _dom_usage_record(dom):
        """
        Provides a complete usage record for the given libvirt domain.
        The return value is a python dict containing this information.
        """
        (record, disks, interfaces) = UsageRecord._dom_xml_info(dom)
        record.update(UsageRecord._dom_disk_io(dom, disks))
        record.update(UsageRecord._dom_network_io(dom, interfaces))
        record.update(UsageRecord._dom_state_cpu_memory(dom))

        return record

    @staticmethod
    def as_json(record):
        return json.dumps(record, sort_keys=True, indent=4)

    def _get_domain(self, uuidstr):
        """
        Retrieves a domain object for the given string UUID.
        """
        return self.connection.lookupByUUIDString(uuidstr)

    def _get_all_domains(self):
        """
        Retrieves all domain objects.
        """
        dom_ids = self.connection.listDomainsID()
        return [self.connection.lookupByID(dom_id) for dom_id in dom_ids]

    def usage_record(self, uuidstr):
        """
        Returns the usage record (as a python dict) for the given
        string UUID.
        """
        dom = self._get_domain(uuidstr)
        return UsageRecord._dom_usage_record(dom)

    def all_usage_records(self):
        """
        Returns a list of usage records (each as a python dict) for
        all of the defined domains.
        """
        doms = self._get_all_domains()
        return [UsageRecord._dom_usage_record(dom) for dom in doms]

