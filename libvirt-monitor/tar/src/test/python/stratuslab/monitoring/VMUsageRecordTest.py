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

import unittest
import json
from stratuslab.monitoring import VMUsageRecord

EXPECTED_FIELDS = set(['name', 'uuid',
                       'vcpu', 'memory', 'cpu_time', 'state',
                       'net_rx', 'net_tx',
                       'disk_read', 'disk_written'])

class VMUsageRecordTest(unittest.TestCase):

    def setUp(self):
        self.vmUsageRecord = VMUsageRecord.VMUsageRecord('test:///default')

    def tearDown(self):
        pass

    def _get_first_dom(self):
        doms = self.vmUsageRecord._get_all_domains()
        return doms.pop()

    def test_get_domains(self):
        doms = self.vmUsageRecord._get_all_domains()
        self.assertEquals(1, len(doms), 'should be one domain defined')

        dom = doms.pop()
        self.assertIsNotNone(dom, 'dom object should not be None')

        uuidstr = dom.UUIDString()
        self.assertIsNotNone(uuidstr, 'UUID should not be None')

        dom_by_uuid = self.vmUsageRecord._get_domain(uuidstr)
        self.assertIsNotNone(dom_by_uuid, 'dom lookup by UUID returned None')

        self.assertEqual(uuidstr, dom_by_uuid.UUIDString(), 'returned dom has wrong UUID')

    def test_network_io(self):
        dom = self._get_first_dom()
        result = VMUsageRecord.VMUsageRecord._dom_network_io(dom, [])
        self.assertEqual(result, {'net_rx': 0L, 'net_tx': 0L})

    def test_disk_io(self):
        dom = self._get_first_dom()
        result = VMUsageRecord.VMUsageRecord._dom_disk_io(dom, [])
        self.assertEqual(result, {'disk_read': 0L, 'disk_written': 0L})

    def test_dom_xml_info(self):
        dom = self._get_first_dom()
        xml, disks, interfaces = VMUsageRecord.VMUsageRecord._dom_xml_info(dom)
        self.assertEqual(0, len(disks), 'test should have no disks')
        self.assertEqual(0, len(interfaces), 'test should have no network interfaces')
        self.assertEqual(dom.name(), xml['name'], 'dict has wrong name value')
        self.assertEqual(dom.UUIDString(), xml['uuid'], 'dict has wrong UUID value')

    def test_dom_state_cpu_memory(self):
        dom = self._get_first_dom()
        result = VMUsageRecord.VMUsageRecord._dom_state_cpu_memory(dom)
        print result['vcpu']
        self.assertLess(0, result['vcpu'], 'invalid vcpu value')
        self.assertLess(0L, result['memory'], 'invalid memory value')
        self.assertLess(0L, result['cpu_time'], 'invalid cpu_time value')
        self.assertEqual('running', result['state'], 'invalid dom state')

    def test_usage_record(self):

        dom = self._get_first_dom()
        uuidstr = dom.UUIDString()

        record = self.vmUsageRecord.usage_record(uuidstr)

        fields = set(record.keys())
        self.assertEqual(fields, EXPECTED_FIELDS, 'invalid record keys')

        json_record = self.vmUsageRecord.as_json(record)
        recreated_record = json.loads(json_record)
        self.assertEqual(record, recreated_record, 'roundtrip through json corrupted data')

    def test_usage_records(self):

        records = self.vmUsageRecord.all_usage_records()
        self.assertEqual(1, len(records), 'wrong number of records returned')
        record = records[0]

        fields = set(record.keys())
        self.assertEqual(fields, EXPECTED_FIELDS, 'invalid record keys')

        json_record = self.vmUsageRecord.as_json(record)
        recreated_record = json.loads(json_record)
        self.assertEqual(record, recreated_record, 'roundtrip through json corrupted data')
