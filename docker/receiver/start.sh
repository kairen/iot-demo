#!/bin/sh
## Receiver docker image start script
# Kyle Bai <kyle.b@inwinstack.com>

echo "API Server : ${K8S_API_SERVER_IP}"
echo "Pod Service Name : ${SERVICE_NAME}"
echo "Pod Name : ${POD_NAME}"
echo "Pod Metadata Namespace : ${POD_NAMESPACE}"

echo "MQTT Remote Server : ${REMOTE_MQTT_IP}"
echo "MQTT Publish Topic : ${MQTT_PUB_TOPIC}"

cd /opt/
export LOCAL_MQTT_IP=$(python discover.py)

echo "MQTT Local Server : ${LOCAL_MQTT_IP}"
python receiver.py
