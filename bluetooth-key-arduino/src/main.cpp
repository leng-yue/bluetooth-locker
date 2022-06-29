#include <Arduino.h>
#include <ArduinoBLE.h>

REDIRECT_STDOUT_TO(Serial)

const int ledPin = LED_BUILTIN;

void setup()
{
  Serial.begin(9600);
  
  // Initialize the LED
  pinMode(ledPin, OUTPUT);

  // Initialize the Battery Level Service
  pinMode(P0_14, OUTPUT);
  digitalWrite(P0_14, LOW);

  // Initialize the BLE module
  if (!BLE.begin())
  {
    Serial.println("failed to initialize BLE!");
    while (1)
      ;
  }

  BLE.setLocalName("Lengyue's Bluetooth Key");
  BLE.advertise();

  Serial.println("Advertising...");
  Serial.println(BLE.address());
}

void loop()
{
  BLE.central();

  // if (BLE.connected())
  // {
  //   digitalWrite(ledPin, LOW);
  // }
  // else
  // {
  //   digitalWrite(ledPin, HIGH);
  // }

  delay(1000);
}
