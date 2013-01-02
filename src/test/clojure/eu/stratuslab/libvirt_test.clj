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
    (is (= v 16))))

(deftest check-num-active-cpus
  (let [v (virt/num-active-cpus test-url)]
    (println "active cpus: " v)
    (is (= v 16))))
