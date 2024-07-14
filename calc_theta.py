import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 물리 상수
G = 6.67430e-11 # 중력 상수, m^3 kg^-1 s^-2

# 초기 조건 설정
mass1 = 5.0 # 물체 1의 질량 (kg)
mass2 = 10.0 # 물체 2의 질량 (kg)
distance = 0.1 # 두 물체 간의 거리 (m)

# 중력 힘 계산 함수
def calculate_gravitational_force(m1, m2, r):
    return G * m1 * m2 / r**2

# 각도 계산 함수 (임의의 스케일로 설정)
def calculate_angle_from_force(force):
    max_force = calculate_gravitational_force(mass1, mass2, 0.05) # 예시 최대 힘
    return min(180, (force / max_force) * 180)

# 시리얼 포트 설정 (포트 번호는 아두이노 연결 포트에 맞게 변경)
ser = serial.Serial('COM3', 9600) # COM 포트는 아두이노 연결 포트에 맞게 변경
time.sleep(2) # 시리얼 포트 안정화를 위한 딜레이

# 그래프 초기 설정
fig, ax = plt.subplots()
ax.set_title('Servo Angles')
line1, = ax.plot([], [], label='Servo 1')
line2, = ax.plot([], [], label='Servo 2')
ax.legend()

# 그래프 데이터 저장
servo1_data = []
servo2_data = []

def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 180)
    return line1, line2

def update(frame):
    global distance
    # 거리와 힘을 변경하는 로직 (예를 들어 거리 감소 시)
    distance -= 0.0001
    if distance < 0.05:
        distance = 0.1

    force = calculate_gravitational_force(mass1, mass2, distance)
    angle1 = calculate_angle_from_force(force)
    angle2 = calculate_angle_from_force(force) # 같은 힘을 두 번째 서보 모터에도 적용

    # 데이터를 시리얼 포트를 통해 아두이노로 전송
    ser.write(f"{angle1},{angle2}\n".encode())

    servo1_data.append(angle1)
    servo2_data.append(angle2)

    if len(servo1_data) > 100:
        servo1_data.pop(0)
    if len(servo2_data) > 100:
        servo2_data.pop(0)

    line1.set_data(range(len(servo1_data)), servo1_data)
    line2.set_data(range(len(servo2_data)), servo2_data)

    return line1, line2

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=100)

plt.tight_layout()
plt.show()
