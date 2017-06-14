#include <Wire.h>
#include <SoftwareSerial.h>
#include "TSYS01.h"
#include <Servo.h>

Servo servoDriver[5];
SoftwareSerial BTSerial(2, 3); // RX | TX
TSYS01 sensor;
String bt_data = String('0');
char inData[50];
char inChar=-1;
byte index = 0;
int servoPins[5] = {0, 1, 2, 3, 4};


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


String servoData; //main captured String
String ser1; //data String
String ser2;
String ser3;
String ser4;
String ser5;
int servoArray[5];

int ind1; // , locations
int ind2;
int ind3;
int ind4;
int ind5;

void loop() {
  if (BTSerial.available())
  {
    //Serial.write(BTSerial.read());
  }
  else
  {
    //sensor.read();
    //String temp(sensor.temperature());
    //Serial.println(temp);
  }

  float cm = 10650.08 * pow(analogRead(0),-0.935) - 10;
while(Serial.available()) 
{

  servoData = Serial.readString();// read the incoming data as string
  
  // Serial.println(servoData);

  ind1 = servoData.indexOf(',');  //finds location of first ,
  ser1 = servoData.substring(0, ind1);   //captures first data String
  ind2 = servoData.indexOf(',', ind1+1 );   //finds location of second ,
  ser2 = servoData.substring(ind1+1, ind2);   //captures second data String
  ind3 = servoData.indexOf(',', ind2+1 );
  ser3 = servoData.substring(ind2+1, ind3);
  ind4 = servoData.indexOf(',', ind3+1 );
  ser4 = servoData.substring(ind3+1,ind4);
  ind5 = servoData.indexOf(',', ind4+1 );
  ser5 = servoData.substring(ind4+1);
  /*
  Serial.println(ser1);
  Serial.println(ser2);
  Serial.println(ser3);
  Serial.println(ser4);
  Serial.println(ser5);
  */
  servoArray[0] = ser1.toInt();
  servoArray[1] = ser2.toInt();
  servoArray[2] = ser3.toInt();
  servoArray[3] = ser4.toInt();
  servoArray[4] = ser5.toInt();

  for(int i = 0; i < 5; i++)
  {
    // Serial.println(servoArray[i]);
    servoDriver[i].writeMicroseconds(servoArray[i]); 
  }
  
}


  //  Stable loop time 15 ms
  loopTime = micros() - timeBegin;
  delayMicroseconds(15000 - loopTime);
  timeBegin = micros();
  Serial.println(cm); 
}
