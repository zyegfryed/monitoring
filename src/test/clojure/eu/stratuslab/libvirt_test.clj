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
(ns eu.stratuslab.libvirt-test
  (:require [eu.stratuslab.libvirt :as virt])
  (:use clojure.test))

(def test-url "test:///default")

(deftest check-num-active-domains
  (let [v (virt/num-active-domains test-url)]
    (println "active domains: " v)
    (is (= v 1))))

(deftest check-num-max-cpus
  (let [v (virt/num-max-cpus test-url)]
    (println "max cpus: " v)
    (is (pos? v))))

(deftest check-num-active-cpus
  (let [v (virt/num-active-cpus test-url)]
    (println "active cpus: " v)
    (is (pos? v))))
