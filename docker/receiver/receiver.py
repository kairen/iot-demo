# coding=utf-8
# Copyright 2017 kyle Bai.
# All Rights Reserved

import os
import json
import commands
import datetime
import psutil
import paho.mqtt.client as mqtt

DEBUG = os.environ.get('DEBUG', 'True')
SUB_SERVER_IP = os.environ.get('LOCAL_MQTT_IP', "192.168.1.103")
SUB_SERVER_PORT = 1883
SUB_TOPIC = "gateway"
SUB_TIMEOUT = 60

PUB_SERVER_IP = os.environ.get('REMOTE_MQTT_IP', "192.168.1.105")
PUB_SERVER_PORT = 1883
PUB_TOPIC = os.environ.get('MQTT_PUB_TOPIC', "Test")

ACCESS_TOKENS = os.environ.get('ACCESS_TOKENS', "GatewayArea1")

attribute_topic = "v1/devices/me/attributes"
telemetry_topic = "v1/devices/me/telemetry"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(SUB_TOPIC)


def on_message(client, userdata, msg):
    mqttc = mqtt.Client("pub")
    mqttc.username_pw_set(ACCESS_TOKENS)
    mqttc.connect(PUB_SERVER_IP, PUB_SERVER_PORT)

    try:
        attr_pl = {
            "kernel_release": commands.getoutput('uname -r'),
            "hardware_architecture": commands.getoutput('uname -m'),
            "operating_system": "HypriotOS",
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent
        }
        data_pl = json.loads(str(msg.payload))
        mqttc.publish(attribute_topic, json.dumps(attr_pl), qos=1)
        mqttc.publish(telemetry_topic, json.dumps(data_pl), qos=1)
        if DEBUG == "True":
            print("{0} : {1}".format(msg.topic, json.dumps(data_pl)))
    except Exception as e:
        print("Message is not JSON format")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(SUB_SERVER_IP, SUB_SERVER_PORT, SUB_TIMEOUT)
client.loop_forever()
