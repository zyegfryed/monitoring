import sys
sys.path.append('/var/lib/stratuslab/python')
import time
import datetime
import json
import requests
from couchbase.client import Couchbase

"""
view defined to get all documents by [uuid, docid], where docid match the format "Accounting..."
Querying views will be performed using REST API endpoint
Method	GET /bucket/_design/design-doc/_view/view-name
Method	PUT /bucket/_design/design-doc
Method	DELETE /bucket/_design/design-doc/_view/view-name
Below: bucket='default', design-doc='dev_byuuidid', and view-name='by_uuidid' 
"""
design_doc = {"views":
              {"by_uuidid":
               {"map":
                '''function (doc, meta) {
		     if (meta.id.indexOf("Accounting") == 0)
			{	
                     		emit([doc.uuid, meta.id], null);
			}
                   }'''
                },
               }
              }

view_tag='_design/dev_byuuidid'

class StratusAccountingHistory(object):
    """
    StratusAccountHistory Class for storing  VMUsage history at instant t. VMUsage(t) = VMUsage(T)-VMUsage(t-1).
    Where VMUsage(T) corresponds to VM total usage, and VMUsage(t-1) the last known VMUsage.
    VMUsage are stored to the Couchbase database.
    An expiry time could be used for VMUsage.
    """

    def __init__(self,
                 host='127.0.0.1:8091', bucket='default', password='', view='_design/dev_byuuidid/_view/by_uuidid'):
        self.host=host
        self.client = Couchbase(host, bucket, password)
        self.bucket = self.client[bucket]
	self.view=view   

    def get_vm_record(self,by_uuid):
        """
        Retrieve VM record from the Couchbase database.
        """
        record = self.bucket.get(by_uuid)
        return record

    def get_vm_usage(self, docid):
        """
        Get VM uuid, disk read and written, state, net_rx, net_tx, vcpu, cpu_time, name and memory.
        """
        vm_usage=json.loads(self.get_vm_record(docid)[2])
  	return vm_usage

    def get_vm_uuid(self, vmrecord):
        """
        Get VM uuid
        """
        vmuuid = vmrecord['uuid']
        return vmuuid

 
    def get_vms_usage_history_byview(self):
        """
        Retrieve all VM usage history, in respect of by_view, from the Couchbase database. 
	All VM usage corresponding to Detlta_t will be computed and returned in as a list. 
        """
        list_vm_usage_delta=[]
	listofview_keys=[]

	rows = self.bucket.view(self.view)

	for row in rows:
                listofview_keys.append(row["key"][0].__str__())

	for key in set(listofview_keys):
		values = self.bucket.view(self.view, startkey=[key,'Accounting/%s' %key], endkey=[key,'Accounting/%s-T' %key])
		values.reverse()

		if len(values) ==1:
			vm_usage_delta = self.get_vm_usage(values[0]['id'])
			list_vm_usage_delta.append(new_record)
		elif len(values) >=2:
			vm_usage_n = self.get_vm_usage(values[0]['id'])
			vm_usage_n_1 = self.get_vm_usage(values[1]['id'])
			vm_usage_delta = self.delta_vm_usages(vm_usage_n, vm_usage_n_1)
			list_vm_usage_delta.append(vm_usage_delta)

        return list_vm_usage_delta



    def publish_history_usage_records(self, records, expiry=0):
        """
	Publish VM usage corresponding to Detlta_t to Couchbase database.
	"""
 
	num_sent = 0
        num_errors = 0
        for record in records:
            try:
                docid, doc = self.docid_and_doc(record)
                self.bucket.set(docid, expiry, 0, doc)
                num_sent += 1
            except Exception:
                num_errors += 1
                pass

        return (num_sent, num_errors)

		
    def docid_and_doc(self, record):
        uuid = record['uuid']
        timest = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        docid =  'Accounting/%s-%s' % (uuid, timest)
        doc = json.dumps(record, sort_keys=True, indent=4)
        return (docid, doc)

    def print_vms_usage(self, record_list):
        for record in record_list:
		for k in record.keys():
			print k + ": " + str(record[k])             		


    def delta_vm_usages(self, vm_usage_n, vm_usage_n_1):
	for i in ['cpu_time','net_tx','net_rx','disk_read','disk_written','memory']:
		vm_usage_n[i]=vm_usage_n[i] - vm_usage_n_1[i]
	return  vm_usage_n

    def create_view(self, view_tag=view_tag, design_doc=design_doc):
        """
        Create view using REST API calls
        """
        view_url='http://%s:8092/default/%s' % (self.host, view_tag)
        data=json.dumps(design_doc)
        headers = {'content-type': 'application/json'}    
        r = requests.put(view_url, data=data, headers=headers)
        print r.text        



    def delete_view(self, view_tag=view_tag):
        """
        Delete view using REST API calls
        """
        view_url='http://%s:8092/default/%s' % (self.host, view_tag)
        headers = {'content-type': 'application/json'}
        r = requests.delete(view_url, headers=headers)
        print r.text


