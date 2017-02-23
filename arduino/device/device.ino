#include <stdio.h>
#include <string.h>
#include <dht.h>
#include <SoftwareSerial.h>
#include <PubSubClient.h>
#include <WiFiEsp.h>
#include <WiFiEspClient.h>
#include <WiFiEspUdp.h>

// Defines
#define DHT_PIN A4
#define PHOTOCELL_PIN 5
#define SSID        "SSID"
#define PASSWORD    "PASSWORD"
#define BUFF_LEN 5

SoftwareSerial wifiSerial(12, 13); /* RX:D3, TX:D2 */
WiFiEspClient espClient;
IPAddress server(192, 168, 1, 103);
PubSubClient client(espClient);
dht DHT;

void callback(char* topic, byte* payload, unsigned int length);
void reconnect();

int status = WL_IDLE_STATUS;
int photocellVal = 0;
static const char *name = "arduino-2";
static const char *topic = "gateway";

void setup() {
  Serial.begin(9600);
  wifiSerial.begin(9600);
  WiFi.init(&wifiSerial);

  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(SSID);
    status = WiFi.begin(SSID, PASSWORD);
  }

  Serial.println("You're connected to the network");
  client.setServer(server, 1883);
  client.setCallback(callback);
}

void loop() {
  photocellVal = analogRead(PHOTOCELL_PIN);
  DHT.read11(DHT_PIN);

  char temp[BUFF_LEN];
  String(DHT.temperature, BUFF_LEN).toCharArray(temp, BUFF_LEN);

  char hum[BUFF_LEN];
  String(DHT.humidity, BUFF_LEN).toCharArray(hum, BUFF_LEN);

  char buffer[100];
  sprintf(buffer, "{\"a2_name\":\"%s\",\"a2_temperature\":%s,\"a2_humidity\":%s,\"a2_photocell\":%d}", name, temp, hum, photocellVal);
  Serial.println(buffer);

  if (!client.connected()) {
    reconnect();
  } else {
    client.publish(topic, buffer);
    client.loop();
  }
  delay(800);
}

//print any message received for subscribed topic
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0; i<length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("arduinoClient")) {
      Serial.println("connected");
//      client.subscribe("presence");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 seconds");
      // Wait 1 seconds before retrying
      delay(1000);
    }
  }
}
