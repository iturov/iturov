#include <Wire.h>

#include "TSYS01.h"

TSYS01 sensor;

void setup() {
  
  Serial.begin(115200);
    
  Wire.begin();

  sensor.init();

}

void loop() {

  sensor.read();
  
  Serial.print(sensor.temperature()); 
  
  delay(100);
}
