(ns eu.stratuslab.monitoring-test
  (:require [metrics.gauges :as mc])
  (:use clojure.test
        eu.stratuslab.monitoring))

(deftest check-num-active-domains-gauge
  (let [v (mc/value num-active-domains)]
    (println "active domains gauge: " v)
    (is (= v 1))))

(deftest check-num-max-cpus-gauge
  (let [v (mc/value num-max-cpus)]
    (println "max cpus gauge: " v)
    (is (= v 16))))

(deftest check-num-active-cpus-gauge
  (let [v (mc/value num-active-cpus)]
    (println "active cpus gauge: " v)
    (is (= v 16))))
