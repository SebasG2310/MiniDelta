import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from model.kinematics import forward_kinematics

def scan_workspace_dk(step=10):
    points = []

    for t1 in range(0, 181, step):
        for t2 in range(0, 181, step):
            for t3 in range(0, 181, step):
                status, position = forward_kinematics(t1, t2, t3)
                if status == 0:
                    points.append(position)

    points = np.array(points)

    if len(points) == 0:
        print("[ERROR] No se encontraron puntos válidos.")
        return

    # Guardar CSV opcional
    np.savetxt("workspace_dk.csv", points, delimiter=",", header="x,y,z", comments='')

    # Graficar
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=5, c='blue')
    ax.set_title("Espacio de trabajo (usando cinemática directa)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

if __name__ == "__main__":
    scan_workspace_dk(step=10)
