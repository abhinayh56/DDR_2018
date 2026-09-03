import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Input")

running = True

while running:

    # Process pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current keyboard state
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        print("UP")

    if keys[pygame.K_DOWN]:
        print("DOWN")

    if keys[pygame.K_LEFT]:
        print("LEFT")

    if keys[pygame.K_RIGHT]:
        print("RIGHT")

    # ESC to quit
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.time.Clock().tick(60)

pygame.quit()