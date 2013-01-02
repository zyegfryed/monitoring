(ns eu.stratuslab.monitoring
  (:require [metrics.gauges :refer [defgauge]]
            [eu.stratuslab.libvirt :as virt]))

(def libvirt-url "test:///default")

(defgauge num-active-domains
  (virt/num-active-domains libvirt-url))

(defgauge num-max-cpus
  (virt/num-max-cpus libvirt-url))

(defgauge num-active-cpus
  (virt/num-active-cpus libvirt-url))
