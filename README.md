
Cloud Monitoring
================

This repository contains the probes and surrounding utilities to
monitor and consolidate cloud resource utilization. 

vmusage code monitor cloud resource utilization.
consolidation code consolidate cloud resource utilization.

Prerequisites
=============

Maven and java are both required to build and test the code.  Install
a certified version of a java virtual machine (1.7 or later) and
maven. 

vmusage code requires that libvirt be available on the build machine.
This can be installed via your machine's packaging system or
manually.  On Mac OSX, homebrew can be used to install libvirt.

All other dependencies are pulled in automatically via the maven
dependency handling mechanism.


Building and Testing
====================

The package uses the standard maven idioms for building and testing:

```
$ mvn clean test
```

for the build and test.  Doing:

```
$ mvn install
```

will fully package the code for deployment.


Installation
============

Install the code via the RPM packages.  There are (or will be)
separate packages for each type of resource.  For example a package
that will be installed on 'host' machines to monitor VM resource
utilization. 


View in consolidation code
==========================
In consolidation code we are using view to get documents from couchbase database.

view defined to get all documents by docid, where docid match the format "Accounting/..."

Querying view performed using REST API endpoint

Method  GET /bucket/_design/design-doc/_view/view-name

Method  PUT /bucket/_design/design-doc

Method  DELETE /bucket/_design/design-doc/_view/view-name

In the consolidation code: bucket='default', design-doc='dev_byid', and view-name='by_id'

The map function:

map_view = {"views":

              {"by_id":

               {"map":

                '''function (doc, meta) {

                     if (meta.id.indexOf("Accounting") == 0)

                        {

                                emit(meta.id, null);

                        }

                   }'''

                },


               }

              }



License
=======

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.
