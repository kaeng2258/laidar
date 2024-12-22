import serial
import cv2
import numpy as np

# Arduino 시리얼 포트 설정 (Arduino 포트와 동일하게 설정)
ser = serial.Serial('COM10', 9600)  # COM 포트와 보드레이트 맞추기
ser.flush()

def get_distance():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if "Distance" in line:
            try:
                distance = int(line.split('=')[1].replace("mm", "").strip())
                return distance
            except ValueError:
                pass
    return None

# 화면 크기 설정
width, height = 640, 480
center = (width // 2, height // 2)

while True:
    # 거리 데이터를 읽어오기
    distance = get_distance()
    
    # 거리 데이터를 기반으로 원의 크기와 색상 조정
    if distance is not None:
        # 거리가 가까울수록 큰 원, 멀수록 작은 원
        radius = max(10, min(200, int(1000 / (distance + 1))))
        
        # 색상 변화: 거리가 가까울수록 빨간색, 멀수록 파란색
        color = (min(255, distance // 4), 0, 255 - min(255, distance // 4))
        
        # 빈 화면 생성
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 화면에 원 그리기
        cv2.circle(frame, center, radius, color, -1)
        
        # 거리 데이터 표시
        cv2.putText(frame, f"Distance: {distance} mm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 화면에 표시
        cv2.imshow("TFMini-S Distance Visualization", frame)
        
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 후 정리
ser.close()
cv2.destroyAllWindows()
