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
from stratuslab.monitoring.vm import UsagePublisher


class UsagePublisherTest(unittest.TestCase):

    def setUp(self):
        self.vmUsagePublisher = UsagePublisher.UsagePublisher(
            libvirt_url='test:///default')

    def tearDown(self):
        pass

    def test_publish_all(self):
        self.vmUsagePublisher.publish_all_usage_records()
