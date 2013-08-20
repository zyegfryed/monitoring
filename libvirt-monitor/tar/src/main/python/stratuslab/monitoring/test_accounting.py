import sys
sys.path.append('/var/lib/stratuslab/python')
from stratuslab.monitoring.StratusAccountingHistory import StratusAccountingHistory



sacc = StratusAccountingHistory(host='onehost-2.lal.in2p3.fr')

(num_sent, num_errors) = sacc.publish_history_usage_records(10)
	
