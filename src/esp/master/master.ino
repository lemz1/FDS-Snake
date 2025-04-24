#include "../include/snake.h"
#include <WiFi.h>
#include <esp_now.h>

void onDataRecv(const esp_now_recv_info_t* info, const uint8_t* incomingData, int len) 
{
  SteuerStationMessage data;
  memcpy(&data, incomingData, sizeof(data));
  
  Serial.print("Bytes received: ");
  Serial.println(len);

  Serial.println(data.button);
}

void setup() 
{
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);

  checkEspRes(esp_now_init(), "Error initializing ESP-NOW");

  esp_now_register_recv_cb(onDataRecv);

  Serial.println("Ready!!!");
}

void loop() {}