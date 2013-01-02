
Test Framework for Virtual Machine Monitoring
=============================================

This code is an experiment to see if metrics can be collected from
libvirt for hypervisors and for virtual machines.

The general idea is to have a process (either a cron or persistent
daemon) collecting information from [libvirt][libvirt] on the
hypervisor.  It then transmits that information to the
[ganglia][ganglia] server for the cloud infrastructure.

This test framework is written in clojure and makes use of both
clojure and java libraries.  Specifically, the following libraries are
used: 

* [Metrics Core][metrics-core-github] ([docs][metrics-core-docs]):
  Framework for defining various metrics and providing methods for
  reporting them
* [metrics-clojure][metrics-clojure]: Thin clojure wrapper for Metric
  Core Java API
* [libvirt Java API][libvirt-java] ([javadoc][libvirt-java-javadocs]):
  Java API that wraps the native C API


Prerequisites
=============

Maven and java are both required to build and test the code.  Install
a certified version of a java virtual machine (1.6 or later) and
maven. 

The code also requires that libvirt be available on the build machine.
This can be installed via your machine's packaging system or
manually.  On Mac OSX, homebrew can be used to install libvirt.

All other dependencies are pulled in automatically via the maven
dependency handling mechanism.


Building and Testing
====================

Maven is used for building and testing the code.  Running the
following command should build and test the code:

```
$ mvn clean test
```

The tests should run successfully and produce output similar to this:

```
Testing eu.stratuslab.monitoring-test
active domains gauge:  1
max cpus gauge:  16
active cpus gauge:  16

Testing eu.stratuslab.libvirt-test
active cpus:  16
active domains:  1
max cpus:  16
```

Note that the CPU information may differ depending on the physical
configuration of your build node. 


Running the Code
================

Currently the code needs to be run from the REPL.  Before starting the
REPL, you'll probably want to change the hypervisor URL.  Change the
variable `libvirt-url` in the `eu.stratuslab.monitoring` namespace to
the URL for your hypervisor. 

The default URL is `test:///default`.  For KVM you'll probably want
something like `qemu:///system`. 

Do the following to start the REPL:

```
mvn clojure:repl
```

and then execute the following commands:

```clojure
(use 'eu.stratuslab.monitoring) 
(import 'com.yammer.metrics.reporting.GangliaReporter)
(import 'java.util.concurrent.TimeUnit)
(GangliaReporter/enable 1 TimeUnit/MINUTES "ganglia.example.com" 8649)
```

This should now be reporting metrics to your ganglia server once per
minute.

[libvirt]: http://libvirt.org
[ganglia]: http://ganglia.sourceforge.net
[metrics-core-github]: https://github.com/codahale/metrics
[metrics-core-docs]: http://metrics.codahale.com
[metrics-clojure]: https://github.com/sjl/metrics-clojure
[libvirt-java]: http://libvirt.org/java.html
[libvirt-java-javadocs]: http://libvirt.org/sources/java/javadoc/

