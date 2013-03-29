#!/usr/bin/env python

import libvirt
import xml.etree.ElementTree as ET
import json

states = {0: 'undefined',
          1: 'running',
          2: 'blocked',
          3: 'paused',
          4: 'shutdown',
          5: 'shutoff',
          6: 'crashed', 
          7: 'pmsuspended',
          8: 'last'}

def netio(dom, interfaces):
    rx_total = 0L
    tx_total = 0L
    for interface in interfaces:
        (rx, _, _, _, tx, _, _, _) =  dom.interfaceStats(interface)
        rx_total += rx
        tx_total += tx
    return {'net_rx': rx_total, 'net_tx': tx_total}

def diskio(dom, disks):
    rbytes_total = 0L
    wbytes_total = 0L
    for disk in disks:
        (_, rbytes, _, wbytes, _) =  dom.blockStats(disk)
        rbytes_total += rbytes
        wbytes_total += wbytes
    return {'disk_read': rbytes_total, 'disk_written': wbytes_total}

def dominfo(dom):
    (state, maxMem_kb, memory_kb, vcpu, cpu_time_ns) = dom.info()
    return {'state': states[state],
            'memory' : memory_kb * 1000L,
            'vcpu': vcpu,
            'cpu_time': cpu_time_ns/1000000000L}

def dominfo_xml(dom):
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

    return {'name': name,
            'uuid': uuid,
            'disks' : disks,
            'interfaces' : interfaces}

def dominfo_json(dom):
    domdesc = dominfo_xml(dom)
    domdesc.update(diskio(dom, domdesc['disks']))
    domdesc.update(netio(dom, domdesc['interfaces']))
    domdesc.update(dominfo(dom))

    return json.dumps(domdesc, sort_keys=True, indent=4)


lvconn = libvirt.open("qemu:///system")

for domid in lvconn.listDomainsID():
    dom = lvconn.lookupByID(domid)
    print dominfo_json(dom)

