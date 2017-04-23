#include <Wire.h>
#include <SoftwareSerial.h>
#include "TSYS01.h"

SoftwareSerial BTSerial(2, 3); // RX | TX
TSYS01 sensor;
String bt_data = String('0');


void setup() {
  
  Serial.begin(115200);

  BTSerial.begin(9600);  
    
  Wire.begin();

  sensor.init();

}

void loop() {
  
  if (BTSerial.available()) 
  {
    Serial.write(BTSerial.read());
  }
  else 
  {
    sensor.read();
    String temp(sensor.temperature());
    Serial.println(temp);
  }
  delay(100);
}
