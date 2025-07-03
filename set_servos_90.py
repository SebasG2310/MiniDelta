from adafruit_pca9685 import PCA9685
import board
import busio
import time

# Inicializar I2C y PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Frecuencia estándar de servos

# RDS3218 acepta pulsos entre 500 µs (0°) y 2500 µs (180°)
def angle_to_duty_us(angle):
    pulse_us = 500 + (angle / 180.0) * (2500 - 500)  # De 500 a 2500 µs
    duty = int((pulse_us / 20000.0) * 65535)         # 20ms ciclo (50Hz)
    return duty

# Mover canales 0, 1 y 2 a 90°
angle =90
duty = angle_to_duty_us(angle)
print(f"Moviendo RDS3218 a 90° (duty: {duty})")

for ch in [0, 1, 2]:
    pca.channels[ch].duty_cycle = duty
    print(f"Canal {ch} → 90°")

time.sleep(1)

# Puedes liberar el PWM si deseas
# for ch in [0, 1, 2]:
#     pca.channels[ch].duty_cycle = 0

pca.deinit()
