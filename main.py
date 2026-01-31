import pygame, sys
from pygame.locals import *

pygame.init()
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600

PLAYER_WIDTH: int = 48
PLAYER_HEIGHT: int = 48

PROJECTILE_WIDTH: int = 48
PROJECTILE_HEIGHT: int = 48

GAP_BELOW_PLAYER: int = 24

BORDERS = 200


class Projectile:
  def __init__(self, x, y, dy):
    self.x = x
    self.y = y
    self.dy = dy

projectiles = []

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# space invader style character at bottom

player_x = WINDOW_WIDTH / 2

pygame.display.set_caption('Masketeer')

while True:  # main game loop

    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # key handling
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_x -= 1
    if keys[K_RIGHT]:
        player_x += 1
    if keys[K_SPACE]:
        # shoot mask
        if not projectiles:
            projectiles.append(Projectile(player_x, WINDOW_HEIGHT - PLAYER_HEIGHT - GAP_BELOW_PLAYER, -1))


    if player_x < BORDERS:
        player_x = BORDERS

    if player_x >= (max_x := (WINDOW_WIDTH - BORDERS - PLAYER_WIDTH)):
        player_x = max_x

    pygame.draw.rect(screen, (100, 100, 100),
                     pygame.Rect(0 + BORDERS, 0, WINDOW_WIDTH - BORDERS - BORDERS, WINDOW_HEIGHT))

    remove_projectiles = []
    for projectile in projectiles:
        projectile.y += projectile.dy
        pygame.draw.rect(screen, (255, 0, 0),
                       pygame.Rect(projectile.x, projectile.y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        if projectile.y < -PROJECTILE_HEIGHT:
            remove_projectiles.append(projectile)
    for projectile in remove_projectiles:
      projectiles.remove(projectile)

    pygame.draw.rect(
        screen,
        "blue",
        (player_x, WINDOW_HEIGHT - PLAYER_HEIGHT - GAP_BELOW_PLAYER, PLAYER_WIDTH, PLAYER_HEIGHT)
    )

    pygame.display.update()
