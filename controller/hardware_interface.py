from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
import time
from model.config import delta_config

class ServoDriver:
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(i2c, address=delta_config["pca9685_address"])
        self.pca.frequency = delta_config["pca9685_freq"]
        self.channels = delta_config["servo_channels"]

    def angle_to_pwm(self, angle):
        pulse_us = 500 + (angle / 180.0) * (2500 - 500)  # De 500 a 2500 µs
        duty = int((pulse_us / 20000.0) * 65535)         # 20ms ciclo (50Hz)
        return duty

    def move_servos(self, angles):
        for ch, angle in zip(self.channels, angles):
            pwm = self.angle_to_pwm(180-angle)
            self.pca.channels[ch].duty_cycle = pwm
        time.sleep(0.01)