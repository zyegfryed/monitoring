import sys
from couchbase import Couchbase
from couchbase.views.iterator import View
from couchbase.views.params import Query

"""
view defined to get all documents by docid, where docid match the format "Accounting..."
Querying views will be performed using REST API endpoint
Method  GET /bucket/_design/design-doc/_view/view-name
Method  PUT /bucket/_design/design-doc
Method  DELETE /bucket/_design/design-doc/_view/view-name
Below: bucket='default', design-doc='dev_stratuslab', and view-name='by_id'
"""
mapreduce_view = {
    "views": {
        "by_id": {
            "map":
'''
function (doc, meta) {
    if (meta.id.indexOf("Accounting") == 0) {
        emit(meta.id, null);
    }
}
'''
        },
    }
}

design_doc='dev_stratuslab'
view_name='by_id'


class Consolidation(object):
    """
    Consolidation Class for storing  VMUsage consolidation at instant t. VMUsage(t) = VMUsage(T)-VMUsage(t-1).
    Where VMUsage(T) corresponds to VM total usage, and VMUsage(t-1) the last known VMUsage.
    VMUsage are stored to the Couchbase database.
    An expiry time could be used for VMUsage.
    """

    def __init__(self, client, uuid):
        self.uuid = uuid
        self.cb = client

    def get_vms_usage_consolidation_byview(self):
        """
        Retrieve all VM usage, in respect of by_view, from the Couchbase database.

        All VM usage corresponding to Detlta_t will be computed and returned in as a list.
        """

        doc_ids = []

        query = Query(
            inclusive_end=True,
            descending=True,
            limit=2,
            debug=True,
            mapkey_range=[
                "Accounting/%s/T" %self.uuid,
                "Accounting/%s/" %self.uuid
            ]
        )

        rows = View(self.cb, design_doc, view_name, query=query)

        for row in rows:
            doc_ids.append(row.docid)

        return self.delta_vm_usages(doc_ids)

    def get_vm_usage(self, docid):
        """
        Get VM uuid, disk read and written, state, net_rx, net_tx, vcpu,
        cpu_time, name and memory.
        """
        vm_usage=self.cb.get(docid).value
        return vm_usage

    def print_vms_usage(self, record_list):
        for record in record_list:
            for k in record.keys():
                print k + ": " + str(record[k])

    def delta_vm_usages(self, doc_ids):
        if len(doc_ids) ==1:
                vm_usage_n = self.get_vm_usage(doc_ids[0])
        elif len(doc_ids) ==2:
                vm_usage_n = self.get_vm_usage(doc_ids[0])
                vm_usage_n_1 = self.get_vm_usage(doc_ids[1])
        for i in ['cpu_time', 'net_tx', 'net_rx', 'disk_read',
                  'disk_written','memory']:
                        vm_usage_n[i]=vm_usage_n[i] - vm_usage_n_1[i]
        return vm_usage_n

    def publish_consolidation_usage_records(self,  expiry=0):
        """
        Publish VM usage corresponding to Detlta_t to Couchbase database.
        """
        record= self.get_vms_usage_consolidation_byview()
        try:
            docid = self._docid(record)
            self.cb.set(docid, record, 0, expiry)
        except Exception:
            pass

    def _docid(self, record):
        uuid = record['uuid']
        timest = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        docid =  'Accounting/%s/%s' % (uuid, timest)
        return docid
