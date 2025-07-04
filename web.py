from flask import Flask, render_template, request
from model.kinematics import inverse_kinematics, forward_kinematics
from controller.motion_controller import MotionController
from input.joystick_controller import run_joystick_mode
from model.config import delta_config
from model.state import RobotState
import csv
import threading
import platform

if platform.system() == "Linux" and "arm" in platform.machine():
    from controller.hardware_interface import ServoDriver
else:
    from controller.hardware_interface_mock import ServoDriver

app = Flask(__name__)

# Inicializar hardware y controlador
driver = ServoDriver()
state = RobotState()
controller = MotionController(driver, state)
controller.initialize_position()

def report(state):
    print(f"[INFO] Ángulos: {state.joint_angles}, Posición: {state.x, state.y, state.z}")
@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/control', methods=['GET', 'POST'])
def index():
    result = None
    mode = "ik"
    if request.method == 'POST':
        mode = request.form.get('mode')

        if mode == 'angles':
            try:
                theta1 = float(request.form['theta1'])
                theta2 = float(request.form['theta2'])
                theta3 = float(request.form['theta3'])
                controller.move_by_angles(theta1, theta2, theta3)
                report(state)
                result = {
                    'x': state.x,
                    'y': state.y,
                    'z': state.z,
                }
            except Exception as e:
                result = {'error': f'Error en cinemática directa: {e}'}

        elif mode == 'coords':
            try:
                x = float(request.form['x'])
                y = float(request.form['y'])
                z = float(request.form['z'])
                controller.move_to(x, y, z)
                report(state)
                result = {
                    'theta1': state.joint_angles[0],
                    'theta2': state.joint_angles[1],
                    'theta3': state.joint_angles[2],
                    'x': x, 'y': y, 'z': z
                }
            except Exception as e:
                result = {'error': f'Error en cinemática inversa: {e}'}

        elif mode == 'trajectory':
            try:
                file_path = request.form['csv_file']
                with open(file_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        x = float(row['x'])
                        y = float(row['y'])
                        z = float(row['z'])
                        controller.move_to(x, y, z)
                result = {'msg': 'Trayectoria ejecutada correctamente.'}
            except Exception as e:
                result = {'error': f'Error ejecutando trayectoria: {e}'}

        elif mode == 'remote':
            try:
                threading.Thread(target=run_joystick_mode, daemon=True).start()
                result = {'msg': 'Modo control remoto iniciado (requiere joystick conectado).'}
            except Exception as e:
                result = {'error': f'Error iniciando control remoto: {e}'}
        elif mode == 'arrows':
            try:
                step = 1
                direction = request.form['dir']
                x, y, z = state.x, state.y, state.z

                if direction == 'up':
                    z += step
                elif direction == 'down':
                    z -= step
                elif direction == 'left':
                    x -= step
                elif direction == 'right':
                    x += step
                elif direction == 'forward':
                    y += step
                elif direction == 'backward':
                    y -= step

                controller.move_to(x, y, z)
                report(state)
            except Exception as e:
                result = {'error': f'Error en flechas: {e}'}

    return render_template('index.html', result=result,config=delta_config,active_section=mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
