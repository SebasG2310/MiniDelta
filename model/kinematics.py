import math
from model.config import delta_config

pi = math.pi
sin120 = math.sin(2 * pi / 3)
cos120 = math.cos(2 * pi / 3)

def delta_calc_angle_yz(x0, y0, z0, f, e, rf, re):
    y1 = -0.5 * 0.57735 * f
    y0 -= 0.5 * 0.57735 * e
    a = (x0**2 + y0**2 + z0**2 + rf**2 - re**2 - y1**2) / (2 * z0)
    b = (y1 - y0) / z0
    discriminant = -(a + b * y1)**2 + rf * (b * b * rf + rf)
    if discriminant < 0:
        return -1, 0.0
    yj = (y1 - a * b - math.sqrt(discriminant)) / (b * b + 1)
    zj = a + b * yj
    theta = math.degrees(math.atan2(-zj, y1 - yj))
    if yj > y1:
        theta += 180.0
    return 0, theta

def inverse_kinematics(x0, y0, z0, f=None, e=None, rf=None, re=None):
    f = f or delta_config["f"]
    e = e or delta_config["e"]
    rf = rf or delta_config["rf"]
    re = re or delta_config["re"]

    status, theta1 = delta_calc_angle_yz(x0, y0, z0, f, e, rf, re)
    if status != 0:
        return -1, [0.0, 0.0, 0.0]

    x1 = x0 * cos120 + y0 * sin120
    y1 = y0 * cos120 - x0 * sin120
    status, theta2 = delta_calc_angle_yz(x1, y1, z0, f, e, rf, re)
    if status != 0:
        return -1, [0.0, 0.0, 0.0]

    x2 = x0 * cos120 - y0 * sin120
    y2 = y0 * cos120 + x0 * sin120
    status, theta3 = delta_calc_angle_yz(x2, y2, z0, f, e, rf, re)
    if status != 0:
        return -1, [0.0, 0.0, 0.0]

    return 0, [theta1, theta2, theta3]