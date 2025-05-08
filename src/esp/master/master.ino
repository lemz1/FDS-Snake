#include "../include/snake.h"
#include <WiFi.h>
#include <esp_now.h>

typedef struct struct_message {
    int button_press;
} struct_message;

struct_message myData;

void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);

  Serial.println(myData.button_press);
}

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_recv_cb(OnDataRecv);

  Serial.println('Ready!!!');
}

void loop() {}
