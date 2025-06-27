class RobotState:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = -100
        self.joint_angles = [90, 90, 90]
        self.error = False

    def update_position(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def update_angles(self, angles):
        self.joint_angles = angles