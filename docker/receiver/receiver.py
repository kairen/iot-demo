# coding=utf-8
# Copyright 2017 kyle Bai.
# All Rights Reserved

import os
import json
import datetime
import paho.mqtt.client as mqtt

SUB_SERVER_IP = os.environ.get('LOCAL_MQTT_IP', "172.20.3.27")
SUB_SERVER_PORT = 1883
SUB_TOPIC = "gateway"
SUB_TIMEOUT = 60

PUB_SERVER_IP = os.environ.get('REMOTE_MQTT_IP', "172.20.3.21")
PUB_SERVER_PORT = 1883
PUB_TOPIC = os.environ.get('MQTT_PUB_TOPIC', "Test")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(SUB_TOPIC)

def on_message(client, userdata, msg):
    mqttc = mqtt.Client("pub")
    mqttc.connect(PUB_SERVER_IP, PUB_SERVER_PORT)
    payload = json.loads(str(msg.payload))
    payload.update({"date": "{0}".format(datetime.datetime.now())})
    mqttc.publish(PUB_TOPIC, json.dumps(payload), qos=1)
    print(msg.topic + ":" + json.dumps(payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(SUB_SERVER_IP, SUB_SERVER_PORT, SUB_TIMEOUT)
client.loop_forever()
