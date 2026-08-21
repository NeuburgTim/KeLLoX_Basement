import pygame

pygame.init()
pygame.joystick.init()

# Controller suchen
if pygame.joystick.get_count() == 0:
    print("Kein Controller gefunden!")
    print("Verbinde deinen PS5-Controller per USB oder Bluetooth.")
    raise SystemExit

controller = pygame.joystick.Joystick(0)
controller.init()

print("Controller gefunden:")
print(controller.get_name())

# Fenster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PS5 Controller Input Viewer")

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

clock = pygame.time.Clock()
running = True


def text(surface, message, x, y, font_obj=font):
    surface.blit(font_obj.render(message, True, (255, 255, 255)), (x, y))


while running:
    # Events verarbeiten
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Button gedrückt
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"BUTTON DOWN: {event.button}")

        # Button losgelassen
        elif event.type == pygame.JOYBUTTONUP:
            print(f"BUTTON UP: {event.button}")

        # Stick / Trigger bewegt
        elif event.type == pygame.JOYAXISMOTION:
            print(
                f"AXIS {event.axis}: "
                f"{controller.get_axis(event.axis):.3f}"
            )

        # D-Pad
        elif event.type == pygame.JOYHATMOTION:
            print(f"D-PAD: {event.value}")

    # Hintergrund
    screen.fill((25, 25, 30))

    text(screen, "PS5 Controller Input Viewer", 30, 25)

    # Buttons
    text(screen, "BUTTONS", 30, 80)

    button_names = {
        0: "X",
        1: "Circle",
        2: "Square",
        3: "Triangle",
        4: "Share",
        5: "PS",
        6: "Options",
        7: "L3",
        8: "R3",
        9: "L1",
        10: "R1",
    }

    y = 120

    for button_id, name in button_names.items():
        if button_id < controller.get_numbuttons():
            pressed = controller.get_button(button_id)

            status = "PRESSED" if pressed else "released"

            text(
                screen,
                f"{button_id:2}  {name:10} {status}",
                30,
                y,
                small_font
            )

            y += 28

    # Achsen
    x_pos = 400

    text(screen, "AXES", x_pos, 80)

    axis_names = {
        0: "Left Stick X",
        1: "Left Stick Y",
        2: "Right Stick X",
        3: "Right Stick Y",
        4: "L2 Trigger",
        5: "R2 Trigger",
    }

    y = 120

    for axis_id, name in axis_names.items():
        if axis_id < controller.get_numaxes():
            value = controller.get_axis(axis_id)

            text(
                screen,
                f"{axis_id}: {name}",
                x_pos,
                y,
                small_font
            )

            text(
                screen,
                f"{value:+.3f}",
                x_pos + 180,
                y,
                small_font
            )

            y += 35

    # D-Pad
    text(screen, "D-PAD", x_pos, 350)

    if controller.get_numhats() > 0:
        hat = controller.get_hat(0)

        text(
            screen,
            f"X: {hat[0]:+d}   Y: {hat[1]:+d}",
            x_pos,
            390,
            small_font
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()