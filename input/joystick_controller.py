def run_joystick_mode():
    import pygame
    pygame.init()
    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            pygame.event.pump()
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            axis_z = joystick.get_axis(3)

            x = axis_x * 30
            y = axis_y * 30
            z = -170 + axis_z * 30

            status, angles = inverse_kinematics(x, y, z)
            if status == 0:
                driver.move_servos(angles)

    except KeyboardInterrupt:
        pygame.quit()