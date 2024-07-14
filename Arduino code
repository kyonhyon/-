#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
  servo1.attach(9); // 첫 번째 서보 모터 핀 번호 (9번 핀에 연결)
  servo2.attach(10); // 두 번째 서보 모터 핀 번호 (10번 핀에 연결)
}

void loop() {
  if (Serial.available() > 0) { // 시리얼 데이터가 들어오면
    String data = Serial.readStringUntil('\n'); // 한 줄 읽기
    int commaIndex = data.indexOf(','); // 콤마 위치 찾기
    int angle1 = data.substring(0, commaIndex).toInt(); // 첫 번째 각도
    int angle2 = data.substring(commaIndex + 1).toInt(); // 두 번째 각도

    servo1.write(angle1); // 첫 번째 서보 모터 제어
    servo2.write(angle2); // 두 번째 서보 모터 제어
  }
  delay(100); // 딜레이
}
