#include <Servo.h>

const int servoPin = 9;

Servo servo;

void setup() {
  servo.attach(servoPin);
  servo.write(90);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    
    if (command == 'H') {
      servo.write(180);  // 인식 시 서보 모터 180
    } else if (command == 'S') {
      servo.write(90);  // 미인식 시 서보 모터 정지
    }
  }
}
