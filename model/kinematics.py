import math
from model.config import delta_config

pi = math.pi
sqrt3 = math.sqrt(3)
tan30 = 1 / sqrt3
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

def forward_kinematics(theta1, theta2, theta3, f=None, e=None, rf=None, re=None):
    f = f or delta_config["f"]
    e = e or delta_config["e"]
    rf = rf or delta_config["rf"]
    re = re or delta_config["re"]

    # Trigonometry constants
    t = (f - e) * tan30 / 2

    # Convert angles to radians
    theta1 = math.radians(theta1)
    theta2 = math.radians(theta2)
    theta3 = math.radians(theta3)

    # Calculate position of each arm's joint
    y1 = -(t + rf * math.cos(theta1))
    z1 = -rf * math.sin(theta1)

    x2 = (t + rf * math.cos(theta2)) * sin120
    y2 = (t + rf * math.cos(theta2)) * cos120
    z2 = -rf * math.sin(theta2)

    x3 = (-t - rf * math.cos(theta3)) * sin120
    y3 = (t + rf * math.cos(theta3)) * cos120
    z3 = -rf * math.sin(theta3)

    # Calculate coordinates of intersection point of three spheres
    dnm = (y2 - y1) * x3 - (y3 - y1) * x2

    w1 = y1**2 + z1**2
    w2 = x2**2 + y2**2 + z2**2
    w3 = x3**2 + y3**2 + z3**2

    # Calculate x, y, z
    a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)
    b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

    a2 = -(z2 - z1) * x3 + (z3 - z1) * x2
    b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0

    a = a1**2 + a2**2 + dnm**2
    b = 2 * (a1 * b1 + a2 * b2 + dnm * z1 * dnm)
    c = b1**2 + b2**2 + dnm**2 * (z1**2 - re**2)

    d = b**2 - 4.0 * a * c
    if d < 0:
        return -1, [0.0, 0.0, 0.0]

    z0 = -0.5 * (b + math.sqrt(d)) / a
    x0 = (a1 * z0 + b1) / dnm
    y0 = (a2 * z0 + b2) / dnm

    return 0, [x0, y0, z0]