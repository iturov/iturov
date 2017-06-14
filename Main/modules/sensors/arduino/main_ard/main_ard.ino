#include <Wire.h>
#include <SoftwareSerial.h>
#include "TSYS01.h"
#include <Servo.h>

Servo servoDriver[5];
SoftwareSerial BTSerial(2, 3); // RX | TX
TSYS01 sensor;
String bt_data = String('0');
int servoPins[5] = {0, 1, 2, 3, 4};

String splitString(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup() {
  Serial.begin(115200);
  BTSerial.begin(9600);
  //Wire.begin();
  //sensor.init();
  for (int i = 0; i < 5; i++){
    servoDriver[i].attach(servoPins[i]);
  }
}
int n = 0;
int loopTime = 0;
int timeBegin = 0;
String serialData;
void loop() {
  if (BTSerial.available())
  {
    Serial.write(BTSerial.read());
  }
  else
  {
    //sensor.read();
    //String temp(sensor.temperature());
    //Serial.println(temp);
  }

  float cm = 10650.08 * pow(analogRead(0),-0.935) - 10;

  if (Serial.available()) serialData = Serial.readString();
  String serialArray[5];
  
  for(int i = 0; i < 5; i++){
    serialArray[i] = splitString(serialData, ",", i);
    servoDriver[i].write(serialArray[i].toInt());
  }
  
  //  Stable loop time 15 ms
  loopTime = micros() - timeBegin;
  delayMicroseconds(15000 - loopTime);
  timeBegin = micros();
  Serial.println(cm); 
}
