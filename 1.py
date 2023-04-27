import cv2
import numpy as np
import torch
import serial

ser = serial.Serial('COM3', 9600)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
cap = cv2.VideoCapture(0)  # 0번 카메라 연결

while True:
    ret, frame = cap.read()  # 프레임 읽기
    if not ret:
        break
    results = model(frame)  # 객체 감지 수행

    # 결과를 처리합니다.
    cx_list = []
    cy_list = []
    person_detected = False
    for detection in results.xyxy[0]:
        # 객체의 위치와 클래스 정보를 가져옵니다.
        x1, y1, x2, y2, conf, cls = detection
        label = model.names[int(cls)]
        # person 객체일 때만 그리기
        if label == 'person':
            # 객체의 위치에 사각형을 그려줍니다.
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # 객체의 클래스 이름과 정확도를 화면에 출력합니다.
            cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)
            person_detected = True  # 사람이 감지되었음을 플래그로 표시

    cv2.imshow('YOLOv5', frame)

    # 사람이 감지되었을 때
    if person_detected:
        ser.write(b'H')
    else:
        ser.write(b'S')

    # 'q' 키를 눌러 종료합니다.
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
