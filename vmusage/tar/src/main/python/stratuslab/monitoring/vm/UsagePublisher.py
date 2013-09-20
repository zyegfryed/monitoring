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
import time
import datetime

from couchbase import Couchbase
from stratuslab.monitoring.vm import UsageRecord


class UsagePublisher(object):

    def __init__(self, libvirt_url='qemu:///system', host='127.0.0.1:8091',
                 bucket='default', password=''):

        self.cb = Couchbase.connect(
            host=host, bucket=bucket, password=password)

        self.vmUsageRecord = UsageRecord.UsageRecord(libvirt_url)

    def _docid(self, record):
        uuid = record['uuid']
        timest = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        docid = 'Accounting/%s/T' % uuid
        return docid

    def publish_all_usage_records(self):
        """
        Publish all VM usage records into the Couchbase database. This
        function returns a tuple with the number records successfully
        sent and the number not sent.
        """
        records = self.vmUsageRecord.all_usage_records()

        num_sent = 0
        num_errors = 0
        for record in records:
            try:
                uuid = self._docid(record)
                self.cb.set(uuid, record, 0, 0)
                num_sent += 1
            except Exception:
                num_errors += 1
                pass

        return (num_sent, num_errors)
