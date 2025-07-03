class ServoDriver:
    def __init__(self):
        print("[MOCK] ServoDriver inicializado (sin hardware)")

    def move_servos(self, angles):
        print(f"[MOCK] Mover servos a ángulos: {angles}")