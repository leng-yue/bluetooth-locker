#include <Arduino.h>
#include <ArduinoBLE.h>


void setup()
{
  Serial.begin(9600);
  
  // Initialize the LED
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);


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

  if (BLE.connected())
  {
    digitalWrite(LEDG, LOW);
    digitalWrite(LEDB, HIGH);
  }
  else
  {
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDB, LOW);
  }

  delay(1000);
}
