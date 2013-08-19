import sys
sys.path.append('/var/lib/stratuslab/python')
import json
import requests
from couchbase.client import Couchbase

"""
view defined to get all documents by id
Querying views will be performed using REST API endpoint
Method	GET /bucket/_design/design-doc/_view/view-name
Method	PUT /bucket/_design/design-doc
Method	DELETE /bucket/_design/design-doc/_view/view-name
Below: bucket='default', design-doc='dev_byid', and view-name='by_id' 
"""
design_doc = {"views":
              {"by_id":
               {"map":
                '''function (doc, meta) {
                     emit(doc.id, null);
                   }'''
                },
               }
              }

view_tag='_design/dev_byid'

class StratusAccounting(object):
    """
    StratusAccount Class for retrieving StratusLab accounting records from Couchbase database
    """
    def __init__(self,
                 host='127.0.0.1:8091', bucket='default', password='', view='_design/dev_byid/_view/by_id'):
        self.host=host
        self.client = Couchbase(host, bucket, password)
        self.bucket = self.client[bucket]
	self.view=view   

    def get_usage_record(self,by_id):
        """
        Retrieve VM usage record from the Couchbase database.
        """
        record = self.bucket.get(by_id)
        return record

    def get_vm_usage(self, docid):
        """
        Get VM uuid, disk read and written, state, net_rx, net_tx, vcpu, cpu_time, name and memory, in json format.
        """

        vm_record=json.loads(self.get_usage_record(docid)[2])
  	return vm_record
 
    def get_vms_usage_byview(self):
        """
        Retrieve all VM usage records, in respect of by_view, from the Couchbase database. 
	A list of records in json format will be returned
        """
        record_list=[]
        records = self.bucket.view(self.view)
        for rec in records:
		vm_record=self.get_vm_usage(rec['id'])
		record_list.append(vm_record)
        return record_list

    def print_vms_usage(self, record_list):
        for record in record_list:
		for k in record.keys():
			print k + ": " + str(record[k])             		


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



#sacc = StratusAccounting(host='onehost-5.lal.in2p3.fr')
#sacc.create_view()
#L=sacc.get_vms_usage_byview(myview)
#sacc.print_vms_usage(L)
