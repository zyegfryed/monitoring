#!/usr/bin/env python

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

import sys
sys.path.append('/var/lib/stratuslab/python')

import os
import ConfigParser

from stratuslab.api import LogUtil
from stratuslab.monitoring.UsagePublisher import UsagePublisher

cfg_filename = 'monitoring.cfg'

def _configure():
    fsroot = os.path.splitdrive(sys.executable)[0] or '/'
    cfg_paths = [os.path.join(os.getcwd(), cfg_filename),
                 os.path.join(os.path.expanduser('~'), '.stratuslab', cfg_filename),
                 os.path.join(fsroot, 'etc', 'stratuslab', cfg_filename)]

    config = ConfigParser.ConfigParser()
    config.add_section('vm_usage')
    config.set('vm_usage', 'bucket', 'default')
    config.set('vm_usage', 'password', '')
    used_cfg_files = config.read(cfg_paths)
    return (config, used_cfg_files)

logger = LogUtil.get_syslog_logger(__name__)

(config, used_cfg_files) = _configure()

logger.debug('publisher read configuration from %s' % str(used_cfg_files))

host = config.get('vm_usage', 'host')
if not host:
    logger.debug('logging host not defined; skipping VM usage logging')
    sys.exit(0)

logger.debug('starting VM usage publishing')

try:
    vmUsagePublisher = UsagePublisher(host=host)
    logger.debug('publishing VM usage to %s' % host)
except Exception as e:
    logger.error('error creating UsagePublisher: %s' % str(e))
    sys.exit(1)

try:
    (num_sent, num_errors) = vmUsagePublisher.publish_all_usage_records()
    logger.info('published %d VM usage records to %s; %d errors' % (num_sent, host, num_errors))
except Exception as e:
    logger.error('error publishing VM usage records: %s' % str(e))
    sys.exit(1)

logger.debug('finished VM usage publishing')
