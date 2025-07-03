from model.kinematics import inverse_kinematics, forward_kinematics

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
    def move_by_angles(self, theta1, theta2, theta3):
        try:
            status, position = forward_kinematics(theta1, theta2, theta3)
            if status == 0:
                self.driver.move_servos([theta1, theta2, theta3])
                self.state.update_angles([theta1, theta2, theta3])
                self.state.update_position(*position)
            else:
                print("[ERROR] Los ángulos no resultan en una posición válida")
                self.state.error = True
        except Exception as e:
            print(f"[ERROR] Movimiento por ángulos fallido: {e}")
            self.state.error = True
    def initialize_position(self):
        from model.config import delta_config
        angles = delta_config["initial_angles"]
        print("[INFO] Inicializando robot...")
        self.driver.move_servos(angles)
        self.state.update_angles(angles)
        # Si sabes la posición XYZ que corresponde a ese ángulo, puedes ponerla aquí también
        print(f"[INFO] Posición inicial aplicada: {angles}")