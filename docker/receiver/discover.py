# coding=utf-8
# Copyright 2017 Kyle Bai
# All Rights Reserved

import os
import sys
import json
import requests
import time


class DiscoverNode():

    def __init__(self):
        self.api_ip = os.environ.get('K8S_API_SERVER_IP', "localhost")
        self.api_port = os.environ.get('K8S_API_SERVER_PORT', 8080)
        self.service_name = os.environ.get('SERVICE_NAME', "emqtt")
        self.namespace = os.environ.get('POD_NAMESPACE', "default")
        self.pod_name = os.environ.get('POD_NAME', "emqtt-2201070840-x9ss6")
        self.url = "http://{0}:{1}/api/v1/namespaces/{2}/endpoints".format(
            self.api_ip,
            self.api_port,
            self.namespace,
        )

    def get_node_name(self):
        try:
            response = requests.get(self.url)
            for item in response.json()["items"]:
                if self.pod_name.find(item["metadata"]["name"]) >= 0:
                    addresses = item["subsets"][0]["addresses"]
                    for addr in addresses:
                        if addr["targetRef"]["name"] == self.pod_name:
                            return addr["nodeName"]
        except Exception as e:
            sys.exit()

    def find(self, node_name):
        url = "{0}/{1}".format(self.url, self.service_name)
        try:
            response = requests.get(url)
            subsets = list()
            if "kind" in response.json():
                if response.json()["kind"] == "Status":
                    sys.exit("ERROR : {0}".format(response.json()["message"]))
                elif response.json()["kind"] == "Endpoints":
                    subsets = response.json()["subsets"]
                    for address in subsets[0]["addresses"]:
                        if address["nodeName"] == node_name:
                            print(address["ip"])
        except Exception as e:
            sys.exit()


def main():
    discover = DiscoverNode()
    discover.find(discover.get_node_name())

if __name__ == '__main__':
    main()
