import pygame

def read_joystick():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    axes = [0.0, 0.0, 0.0]
    try:
        while True:
            pygame.event.pump()
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            z = joystick.get_axis(3)
            yield x, y, z
    except KeyboardInterrupt:
        pygame.quit()