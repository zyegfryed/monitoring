import sys
sys.path.append('/var/lib/stratuslab/python')
import time
import datetime
import json
import requests
from couchbase.client import Couchbase
from stratuslab.monitoring import StratusAccountingHistory


class StratusAccountingHistoryPublish(object):

    def __init__(self,
                 host='127.0.0.1:8091', bucket='default', password=''):
        self.host=host
        self.client = Couchbase(host, bucket, password)
        self.bucket = self.client[bucket]

	self.vmUsageHistory = StratusAccountingHistory.StratusAccountingHistory(host)

    def publish_history_usage_records(self,  expiry=0):
        """
	Publish VM usage corresponding to Detlta_t to Couchbase database.
	"""
	records= self.vmUsageHistory.get_vms_usage_history_byview() 
	num_sent = 0
        num_errors = 0
        for record in records:
            try:
                docid, doc = _docid_and_doc(record)
                self.bucket.set(docid, expiry, 0, doc)
                num_sent += 1
            except Exception:
                num_errors += 1
                pass

        return (num_sent, num_errors)

		
    def _docid_and_doc(record):
        uuid = record['uuid']
        timest = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        docid =  'Accounting/%s-%s' % (uuid, timest)
        doc = json.dumps(record, sort_keys=True, indent=4)
        return (docid, doc)



