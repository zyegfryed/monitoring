(ns eu.stratuslab.libvirt
  (:import [org.libvirt Connect]))

(declare ^:dynamic *libvirt-connection*)

(defn connect
  "creates a read-only connection to indicated hypervisor"
  [url]
  (Connect. url false))

(defmacro with-libvirt-url
  "sets the hypervisor to use for libvirt"
  [url & body]
  `(binding [*libvirt-connection* (connect ~url)]
     (let [result# (do ~@body)]
       (.close *libvirt-connection*)
       result#)))

(defn num-active-domains
  "returns number of active (running) domains (VMs)"
  [url]
  (with-libvirt-url url
    (let [connection (connect url)]
      (.numOfDomains connection))))

(defn num-max-cpus
  "returns maximum number of CPUs available on node"
  [url]
  (with-libvirt-url url
    (let [connection (connect url)
          node-info (.nodeInfo connection)]
      (.maxCpus node-info))))

(defn num-active-cpus
  "returns number of active CPUs on node"
  [url]
  (with-libvirt-url url
    (let [connection (connect url)
          node-info (.nodeInfo connection)]
      (.cpus node-info))))
