#include "../include/snake.h"
#include <WiFi.h>
#include <esp_now.h>

// change this to the actual button mac adresses
uint8_t broadcastAddresses[][6] = {
  {0x24, 0x62, 0xab, 0xf2, 0x17, 0x04},
};

#define NUM_BUTTONS (sizeof(broadcastAddresses) / sizeof(broadcastAddresses[0]))

void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData,
                int len) {
  SteuerStationMessage data;
  memcpy(&data, incomingData, sizeof(data));
  Serial.print("Bytes received: ");
  Serial.println(len);

  Serial.println(data.button);
}

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success"
                                                : "Delivery Fail");
}

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  checkEspRes(esp_now_init(), "Error initializing ESP-NOW");

  esp_now_register_recv_cb(onDataRecv);

  Serial.println("Ready!!!");

  esp_now_register_send_cb(onDataSent);

  for (size_t i = 0; i < NUM_BUTTONS; i++) {
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, broadcastAddresses[i], 6 * sizeof(uint8_t));
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    checkEspRes(esp_now_add_peer(&peerInfo), "Failed to add peer");
  }
}

void loop() {
  delay(3000);

  SteuerStationMessage data;
  data.button = GREEN_BUTTON; // temp value

  for (size_t i = 0; i < NUM_BUTTONS; i++) {
    esp_now_send(broadcastAddresses[i], (uint8_t *)&data, sizeof(data));
  }
}
