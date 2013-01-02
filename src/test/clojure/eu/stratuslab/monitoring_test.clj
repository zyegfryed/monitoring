(ns eu.stratuslab.monitoring-test
  (:require [metrics.gauges :as mc])
  (:use clojure.test
        eu.stratuslab.monitoring))

(deftest check-active-vms-gauge
  (let [v (mc/value active-vms)]
    (println v)
    (println (mc/value active-vms))
    (is (< v 20))
    (is (pos? v))))

