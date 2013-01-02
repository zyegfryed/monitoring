(ns eu.stratuslab.monitoring
  (:require [metrics.gauges :refer [defgauge]])
  (:import [org.libvirt Connect]
           [org.libvirt DomainInfo$DomainState]))

(defn test-conn []
  (Connect. "test:///default" false))

(defn get-domain-state-by-id [conn id]
  (let [domain (.domainLookupByID conn id)
        info (.getInfo domain)
        state (.state info)]
    state))

(defn get-active-vms
  ([]
     (get-active-vms (test-conn)))
  ([conn]
     (let [ids (.listDomains conn)
           states (map (partial get-domain-state-by-id conn) ids)
           filtered (filter #(= DomainInfo$DomainState/VIR_DOMAIN_RUNNING %) states)
           running (count filtered)]
       running)))

(defgauge active-vms
  (get-active-vms))
