import pygame, sys
from pygame.locals import *

pygame.init()

WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# space invader style character at bottom

player_x = WINDOW_WIDTH / 2


pygame.display.set_caption('Hello World!')

while True: # main game loop

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

  if player_x < 0:
    player_x = 0

  if player_x >= WINDOW_WIDTH:
    player_x = WINDOW_WIDTH

  pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

  pygame.draw.circle(screen, "red", (player_x, 100), 100)

  pygame.display.update()

