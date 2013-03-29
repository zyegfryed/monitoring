
Cloud Monitoring
================

This repository contains the probes and surrounding utilities to
monitor cloud resource utilization. 


Prerequisites
=============

Maven and java are both required to build and test the code.  Install
a certified version of a java virtual machine (1.7 or later) and
maven. 

The code also requires that libvirt be available on the build machine.
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
