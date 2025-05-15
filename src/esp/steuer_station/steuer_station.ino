#include "../include/snake.h"
#include <WiFi.h>
#include <esp_now.h>

#define BUTTON_PIN 21

#define BUTTON_TYPE GREEN_BUTTON

uint8_t broadcastAddress[] = {0x24, 0x62, 0xab, 0xf2, 0x17, 0x04};

int currentState;
int lastState = HIGH;
esp_now_peer_info_t peerInfo;

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success"
                                                : "Delivery Fail");
}

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("Start");

  WiFi.mode(WIFI_STA);

  checkEspRes(esp_now_init(), "Error initializing ESP-NOW");

  esp_now_register_send_cb(onDataSent);

  memcpy(peerInfo.peer_addr, broadcastAddress, 6 * sizeof(uint8_t));
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  checkEspRes(esp_now_add_peer(&peerInfo), "Failed to add peer");
}

void loop() {
  currentState = digitalRead(BUTTON_PIN);

  if (lastState == HIGH && currentState == LOW) {
    SteuerStationMessage data;
    data.button = BUTTON_TYPE;
    checkEspRes(esp_now_send(broadcastAddress, (uint8_t *)&data, sizeof(data)), "Error sending the data");
  }

  lastState = currentState;
}
