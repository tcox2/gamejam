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
TIME = 0
AFTER_WHAT_TIME_NEW_GUEST_VISITS = 3000
LAST_TIME_NEW_QUEST_VISITS = 0
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
WHITE = (255, 255, 255)

GREEN = (0, 255, 0)

BLUE = (0, 0, 128)
pygame.display.set_caption('Masketeer')
fontObj = pygame.font.Font('freesansbold.ttf', 32)


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

    TIME = pygame.time.get_ticks()
    textSurfaceObj = fontObj.render(str(TIME), True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)
    screen.blit(textSurfaceObj, textRectObj)

    delta = TIME - LAST_TIME_NEW_QUEST_VISITS
    print(TIME, LAST_TIME_NEW_QUEST_VISITS, delta)
    if delta > AFTER_WHAT_TIME_NEW_GUEST_VISITS:
      LAST_TIME_NEW_QUEST_VISITS = TIME


    pygame.draw.rect(
        screen,
        "blue",
        (player_x, WINDOW_HEIGHT - PLAYER_HEIGHT - GAP_BELOW_PLAYER, PLAYER_WIDTH, PLAYER_HEIGHT)
    )

    pygame.display.update()
