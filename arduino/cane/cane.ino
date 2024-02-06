/* This example shows how to take
range measurements with the VL53L0X and display on a SSD1306 OLED.

The range readings are in units of mm. */

#include <Wire.h>
#include "Adafruit_VL53L0X.h"
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display = Adafruit_SSD1306();

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

#if (SSD1306_LCDHEIGHT != 32)
 #error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

void setup()
{
  delay(1000);
  Serial.begin(9600);
  Serial.println("Laser Cane v0.1");

  display.setRotation(2);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  // init done
  display.display();
  delay(500);
  display.setTextColor(WHITE);
  display.clearDisplay();
  display.setCursor(0,0);
  display.print("Laser Cane v0.1");
  display.display();
  delay(1000);

  Wire.begin();

  byte error, address;
  for(address = 1; address < 127; address++ ) 
  {
    // Serial.print("scanning: ");
    // Serial.println(address);
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address<16) 
        Serial.print("0");
      Serial.print(address,HEX);
      Serial.println("  !");
    }
  }
  
  

  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }

  // text display big!
  display.setTextSize(3);
}

void loop()
{
  VL53L0X_RangingMeasurementData_t measure;

  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if (measure.RangeStatus != 4) {  // phase failures have incorrect data
      display.clearDisplay();
      display.setCursor(0,0);
      display.print(measure.RangeMilliMeter);
      display.print("mm");
      display.display();
      delay(50);
  } else {
    display.display();
    display.clearDisplay();
    return;
  }
}