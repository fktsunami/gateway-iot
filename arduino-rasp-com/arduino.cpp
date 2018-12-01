#include <Arduino.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  char data_buffer[120];  
  
  char lat[] = "35.123456789";
  char lng[] = "137.123456789";
  char sensorID[] = "TSUNAMI002";
  char force[] = "100";
  char gyroscope_x[] = "200";
  char gyroscope_y[] = "400";
  char gyroscope_z[] = "500";
  sprintf(data_buffer, "%s-%s-%s-%s-%s-%s-%s", sensorID, lat, lng, force, gyroscope_x, gyroscope_y, gyroscope_z);

  // String lat = "35.123456789";
  // String lng = "137.123456789";
  // String sensorID = "sensor001";
  // String data = "";
  // data += lat;
  // data += '-'
  // Serial.println(data);    
  // 
  // sprintf(data_buffer, "%s", a.c_str());

 
  Serial.println(data_buffer);
  delay(1000);
}