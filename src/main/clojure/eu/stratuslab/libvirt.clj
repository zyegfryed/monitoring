;;
;; Copyright (c) 2010, Centre Nationale de la Recherche Scientifique
;;
;; Licensed under the Apache License, Version 2.0 (the "License");
;; you may not use this file except in compliance with the License.
;; You may obtain a copy of the License at
;;
;; http://www.apache.org/licenses/LICENSE-2.0
;;
;; Unless required by applicable law or agreed to in writing, software
;; distributed under the License is distributed on an "AS IS" BASIS,
;; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;; See the License for the specific language governing permissions and
;; limitations under the License.
;;
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
