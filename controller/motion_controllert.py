from model.kinematics import inverse_kinematics

class MotionController:
    def __init__(self, driver, state):
        self.driver = driver
        self.state = state

    def move_to(self, x, y, z):
        try:
            status, angles = inverse_kinematics(x, y, z)
            if status == 0:
                self.driver.move_servos(angles)
                self.state.update_angles(angles)
                self.state.update_position(x, y, z)
            else:
                print("[ERROR] Posición fuera del alcance")
                self.state.error = True
        except Exception as e:
            print(f"[ERROR] Movimiento fallido: {e}")
            self.state.error = True