#pragma once

#include <WiFi.h>
#include <assert.h>
#include <esp_now.h>
#include <stdint.h>

enum SteuerStationButton {
  GREEN_BUTTON = 0,
  YELLOW_BUTTON = 1,
  RED_BUTTON = 2,
  BLUE_BUTTON = 3,

  // currently unsued, might be relevant in the future
  // WHITE_BUTTON = 4,
};

struct SteuerStationMessage {
  SteuerStationButton button;
};

#define checkEspRes(res, msg)                                                  \
  if (res != ESP_OK) {                                                         \
    Serial.print("(File: ");                                                   \
    Serial.print(__FILE__);                                                    \
    Serial.print(", Line: ");                                                  \
    Serial.print(__LINE__);                                                    \
    Serial.print("): ");                                                       \
    Serial.print("[ESP Now] Failed with error code ");                         \
    Serial.print(res);                                                         \
    Serial.print(": ");                                                        \
    Serial.println(msg);                                                       \
  }
