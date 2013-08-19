import sys
sys.path.append('/var/lib/stratuslab/python')
from stratuslab.monitoring.StratusAccountingCons import StratusAccountingCons

fedcloud_outputfile='0000000001'





sacc = StratusAccountingCons(host='onehost-2.lal.in2p3.fr')

record_list=sacc.get_vms_usage_byview()
(num_sent, num_errors) = sacc.publish_history_usage_records(record_list)
print "num_sent=", num_sent
print "num_errors=", num_errors
f = open(fedcloud_outputfile, 'w')
for record in record_list:
	f.write('%%%%%%\n')
	for k in record.keys():
		f.write(k + ": " + str(record[k]) + '\n')
f.close()
	
