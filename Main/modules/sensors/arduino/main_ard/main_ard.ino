#include <Wire.h>
#include <SoftwareSerial.h>
#include <Servo.h>

Servo servoDriver[5];
SoftwareSerial BTSerial(4, 5); // RX | TX
String bt_data = String('0');
char inData[50];
char inChar=-1;
byte index = 0;
int servoPins[4] = {9, 7, 8, 10};

void setup() {
  Serial.begin(115200);
  BTSerial.begin(9600);
  Serial.setTimeout(50);
  pinMode(11, OUTPUT);
  //Wire.begin();
  //sensor.init();
  for (int i = 0; i < 4; i++){
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
int servoArray[5] = {0, 0, 0, 0, 0};

int ind1; // , locations
int ind2;
int ind3;
int ind4;
int ind5;

int limit(int value, int minimum, int maximum){
  if (value > maximum) value = maximum;
  if (value < minimum) value = minimum;
  return value;
}

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

}


  for(int i = 0; i < 4; i++)
  {
    //Serial.print(i);
    //Serial.print(":");
    //Serial.print(servoArray[i]);
    //Serial.print("\t");
    servoDriver[i].writeMicroseconds(servoArray[i]);
  }
  servoArray[0] = limit(servoArray[0], 1800, 2300);
  servoArray[1] = limit(servoArray[1], 500, 2400);
  servoArray[2] = limit(servoArray[2], 500, 2400);
  servoArray[3] = limit(servoArray[3], 1200, 2000);
  //servoArray[4] = limit(servoArray[4], 1000, 1700);
  if(servoArray[4] == 0) { digitalWrite(11, LOW); }
  else { digitalWrite(11, HIGH); }

  // Serial.println("");


  //  Stable loop time 15 ms
  loopTime = micros() - timeBegin;
  delayMicroseconds(15000 - loopTime);
  timeBegin = micros();
  Serial.println(cm);
  Serial.flush();
}
