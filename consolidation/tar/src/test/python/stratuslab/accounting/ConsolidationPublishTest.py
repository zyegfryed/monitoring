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
from stratuslab.accounting import ConsolidationPublish

vm_uuid=''
expiry=60

class ConsolidationPublishTest(unittest.TestCase):

    def setUp(self):
        self.vmUsageConsolidation = ConsolidationPublish.ConsolidationPublish(vm_uuid, host='localhost')

    def tearDown(self):
        pass

    def test_publish_all(self):
	(num_sent, num_errors) = self.vmUsageConsolidation.publish_consolidation_usage_records(expiry)
	print "num_sent=", num_sent
	print "num_errors=", num_errors
