from flask import Flask, render_template, request
from model.kinematics import inverse_kinematics, forward_kinematics
from controller.hardware_interface import ServoDriver
from controller.motion_controller import MotionController
from input.joystick_controller import run_joystick_mode
from model.config import delta_config
from model.state import RobotState
import csv
import threading

app = Flask(__name__)

# Inicializar hardware y controlador
driver = ServoDriver()
state = RobotState()
controller = MotionController(driver, state)
controller.initialize_position()

def report(state):
    print(f"[INFO] Ángulos: {state.angles}, Posición: {state.position}")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

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

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
