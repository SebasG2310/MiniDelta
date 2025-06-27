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
        pulse_length = 1000000 / self.pca.frequency / 4096
        pulse = (angle * (500/90)) + 1500
        return int(pulse / pulse_length)

    def move_servos(self, angles):
        for ch, angle in zip(self.channels, angles):
            pwm = self.angle_to_pwm(angle)
            self.pca.channels[ch].duty_cycle = pwm << 4
        time.sleep(0.05)