import sys
import time
import datetime
import json
from couchbase import Couchbase
from stratuslab.accounting import Consolidation

class ConsolidationPublish(object):

    def __init__(self,
                 uuid, host='127.0.0.1', bucket='default', password=''):
        
        self.cb = Couchbase.connect(host=host, bucket=bucket, password=password)

	self.vmUsageConsolidation = Consolidation.Consolidation(self.cb,uuid)


    def publish_consolidation_usage_records(self,  expiry=0):
        """
	Publish VM usage corresponding to Detlta_t to Couchbase database.
	"""
	record= self.vmUsageConsolidation.get_vms_usage_consolidation_byview() 
	print "record_to_publish=", record
	num_sent = 0
        num_errors = 0
        try:
            docid = self._docid(record)
            self.cb.set(docid, record, 0, expiry)
            num_sent += 1
        except Exception:
            num_errors += 1
            pass
      	return (num_sent, num_errors)

		

    def _docid(self, record):
    	uuid = record['uuid']
    	timest = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
    	docid =  'Accounting/%s/%s' % (uuid, timest)
    	return docid