#include "../include/snake.h"
#include <WiFi.h>
#include <esp_now.h>

const char* buttonNames[] = {
  "UP",     // 0
  "RIGHT",  // 1
  "DOWN",   // 2
  "LEFT"    // 3
};

void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
  SteuerStationMessage data;
  memcpy(&data, incomingData, sizeof(data));
  
  if (data.button >= 0 && data.button <= 3) {
    Serial.println(buttonNames[data.button]);
  } else {
    Serial.print("Unbekannter Button-Wert: ");
    Serial.println(data.button);
  }
}

void setup() {
  Serial.begin(115200);
  
  WiFi.mode(WIFI_STA);
  checkEspRes(esp_now_init(), "Error initializing ESP-NOW");

  esp_now_register_recv_cb(onDataRecv);
}

void loop() {}
