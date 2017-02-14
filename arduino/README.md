# Arduino Device


## Requirement
* WiFiEsp
* PubSubClient
* dht

# ESP8266 AT SDK
Flash esp8266 soc using the follow command:
```sh
$ esptool.py -p /dev/cu.usbserial write_flash 0x0 ESP8266_AT25-SDK112-512k.bin
```
