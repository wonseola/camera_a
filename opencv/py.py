import cv2
import numpy as np
import time
import serial

arduino = serial.Serial('COM3', 9600) # 아두이노와의 시리얼 통신 설정

cap = cv2.VideoCapture(0) # 웹캠 사용
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml') # 얼굴 인식용 분류기 로드

servo_position = 0 # 서보모터 시작 위치
servo_range = 90 # 서보모터 움직임 범위

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    # 인식된 얼굴이 있으면
    
    if len(faces) > 0:
        arduino.write(b'H') # 아두이노에 H 전송
        time.sleep(0.1) # 시간 지연
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            # 얼굴 중심 계산
            center_x = x + w//2
            # 서보모터 움직임 계산
            angle = int(np.interp(center_x, [0, 640], [servo_position - servo_range, servo_position + servo_range]))
            # 아두이노에 움직임 값 전송
            arduino.write(str(angle).encode())
            arduino.write(b'\n')
            time.sleep(0.1) # 시간 지연
    else:
        arduino.write(b'L') # 아두이노에 L 전송
        time.sleep(0.1) # 시간 지연
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# 서보모터 원위치로 돌리기
arduino.write(b'90\n')
