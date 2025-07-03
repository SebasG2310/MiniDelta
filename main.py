from model.state import RobotState
from controller.hardware_interface import ServoDriver
from controller.motion_controller import MotionController
from view.telemetry import report
from model.config import delta_config
from input.xbox_controller import read_joystick
import csv
import threading

USE_JOYSTICK = False

if __name__ == '__main__':
    state = RobotState()
    driver = ServoDriver()
    controller = MotionController(driver, state)
    controller.initialize_position()

    if USE_JOYSTICK:
        print("Modo joystick activado. CTRL+C para salir.")
        for x, y, z in read_joystick():
            scaled_x = x * 100
            scaled_y = y * 100
            scaled_z = -z * 200 - 300
            controller.move_to(scaled_x, scaled_y, scaled_z)
            report(state)

    else:
        while True:
            cmd = input("Comando (XYZ / archivo / salir): ").strip().lower()
            if cmd == "salir":
                break
            elif cmd == "archivo":
                try:
                    with open(delta_config["trajectory_file"], newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            try:
                                x, y, z = map(float, row)
                                controller.move_to(x, y, z)
                                report(state)
                            except Exception as e:
                                print(f"[ERROR] Línea inválida: {row} → {e}")
                except FileNotFoundError:
                    print("[ERROR] Archivo de trayectoria no encontrado.")
            else:
                try:
                    x, y, z = map(float, cmd.split())
                    controller.move_to(x, y, z)
                    report(state)
                except ValueError:
                    print("[ERROR] Entrada inválida. Usa: X Y Z o 'archivo' o 'salir'")
