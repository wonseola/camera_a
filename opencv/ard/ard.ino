#include <Servo.h>

Servo myservo;
int pos = 90;

void setup() {
  myservo.attach(9);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char val = Serial.read(); // 시리얼에서 데이터 읽기
    if (val == 'H') { // H가 오면 서보모터 움직이기
    Serial.write("H");
      for (pos = 0; pos <= 90; pos += 1) {
        myservo.write(pos);
        delay(5);
      }
      for (pos = 90; pos >= 0; pos -= 1) {
        myservo.write(pos);
        delay(5);
      }
      for (pos = 0; pos <= 90; pos += 1) {
        myservo.write(pos);
        delay(5);
      }
    } else if (val == 'L') { // L이 오면 서보모터 멈추기
    Serial.write("L");
      myservo.write(0);
    } else {
      char val = Serial.read();
      pos = atoi(&val);
      myservo.write(pos);
    }
  }
}
