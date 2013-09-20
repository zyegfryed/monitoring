from couchbase import Couchbase
from couchbase.views.iterator import View
from stratuslab.accounting import Consolidation


map_view = {
    "views": {
        "by_runningvms": {
            "map":
'''
function (doc, meta) {
    if (meta.id.indexOf("Accounting") == 0 && doc.state == "running") {
        emit(doc.uuid, null);
    }
}
'''
        },
    }
}
view_name='by_runningvms'
design_doc='dev_stratuslab'


class ConsolidationPublish(object):

    def __init__(self, host='127.0.0.1', bucket='default', password=''):
        self.cb = Couchbase.connect(
            host=host, bucket=bucket, password=password)

    def get_all_docuuid_byview(self):
        doc_uuids = []

        rows = View(self.cb, design_doc, view_name)

        for row in rows:
            doc_uuids.append(row.key)
        return set(doc_uuids)

    def publish_all_consolidation_usage_records(self, expiry=0):
        num_sent = 0
        num_errors = 0
        for uuid in  self.get_all_docuuid_byview():
            try:
                Consolidation.Consolidation(self.cb,uuid).publish_consolidation_usage_records(expiry)
                num_sent += 1
            except Exception:
                num_errors += 1
                pass
        return (num_sent, num_errors)

