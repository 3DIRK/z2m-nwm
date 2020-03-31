import os
import logging
import sys

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

import graphviz

from bottle import route, run, template, response, request


def get_parameters():
    parameter_dict = {}
    mand_params = ["USERNAME", "PASSWORD", "HOSTNAME"]
    opt_params = {"PORT": 1883, "LISTEN": 80, "ROOT_TOPIC": "zigbee2mqtt"}

    for item in mand_params:
        try:
            var = os.environ[item]
        except KeyError as keyo:
            logging.error((" ".join(["Environmnet Variable", str(keyo), "is not defined. Stopping!"])))
            sys.exit(1)
        parameter_dict.update({item: var})

    for key, value in opt_params.items():
        try:
            var = os.environ[key]
        except KeyError as keyo:
            logging.warning((" ".join(["Environmnet Variable", str(keyo), "is not defined. Using default!"])))
            var = value
        parameter_dict.update({key: var})
    return parameter_dict


def create_map(topic):
    paras = get_parameters()
    cred = {'username': paras["USERNAME"], 'password': paras["PASSWORD"]}
    publish.single(topic=topic, payload="graphviz", hostname=paras["HOSTNAME"], auth=cred)
    topic_subscribe = "".join([get_parameters()["ROOT_TOPIC"], "/bridge/networkmap/graphviz"])
    message = subscribe.simple(topic_subscribe, hostname=paras["HOSTNAME"], auth=cred)
    network_map = graphviz.Source(message.payload.decode("utf-8"), engine="circo")
    nwm = (network_map.pipe(format="svg", renderer="cairo", formatter="cairo")).decode("utf-8")
    return nwm

@route("/")
def networkmap():
    topic = "".join([get_parameters()["ROOT_TOPIC"], "/bridge/networkmap"])
    response.content_type = "image/svg+xml; charset=utf-8"
    nwm = create_map(topic)
    return nwm

@route("/routes")
def networkroutes():
    topic = "".join([get_parameters()["ROOT_TOPIC"], "/bridge/networkmap/routes"])
    response.content_type = "image/svg+xml; charset=utf-8"
    nwm = create_map(topic)
    return nwm


if __name__ == "__main__":
    run(host="0.0.0.0", port=get_parameters()["LISTEN"])
