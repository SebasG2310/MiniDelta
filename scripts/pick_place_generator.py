import csv
import numpy as np

# Configuración de rango de movimiento
x_pick, y_pick = -50, -50
x_place, y_place = 50, 50
z_up = -170
z_down = -200

# Trayectoria simulada tipo pick & place
trajectory = [
    [x_pick, y_pick, z_up],     # 1. Ir arriba del objeto
    [x_pick, y_pick, z_down],   # 2. Bajar a agarrar
    [x_pick, y_pick, z_up],     # 3. Subir con objeto
    [x_place, y_place, z_up],   # 4. Ir al lugar de colocación
    [x_place, y_place, z_down], # 5. Bajar a dejar
    [x_place, y_place, z_up],   # 6. Subir de nuevo
]

# Guardar como CSV
with open("pick_and_place.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["x", "y", "z"])
    writer.writerows(trajectory)

print("[INFO] Trayectoria pick & place guardada como pick_and_place.csv")