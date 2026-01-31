from ctypes.macholib.dylib import dylib_info

import pygame, sys
from pygame.locals import *
import random

DEBUG: bool = False

pygame.init()
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600

PLAYER_WIDTH: int = 48
PLAYER_HEIGHT: int = 48

GUEST_WIDTH: int = 48
GUEST_HEIGHT: int = 48

PROJECTILE_WIDTH: int = 48
PROJECTILE_HEIGHT: int = 48

GAP_BELOW_PLAYER: int = 24
time = 0
AFTER_WHAT_TIME_NEW_GUEST_VISITS = 3000
BORDERS = 200

last_time_new_guest_visits = 0

class Projectile:
  def __init__(self, x, y, dy):
    self.x = x
    self.y = y
    self.dy = dy

projectiles = []

class Guest:
  def __init__(self, x, y, dy):
    self.x = x
    self.y = y
    self.dy = dy

guests = []

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# space invader style character at bottom

player_x = WINDOW_WIDTH / 2
WHITE = (255, 255, 255)
LIGHT_GREY = (100, 100, 100)
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

    pygame.draw.rect(screen, LIGHT_GREY,
                     pygame.Rect(0 + BORDERS, 0, WINDOW_WIDTH - BORDERS - BORDERS, WINDOW_HEIGHT))

    remove_projectiles = []
    for projectile in projectiles:
        projectile.y += projectile.dy
        pygame.draw.rect(screen, "yellow",
                       pygame.Rect(projectile.x, projectile.y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        if projectile.y < -PROJECTILE_HEIGHT:
            remove_projectiles.append(projectile)
    for projectile in remove_projectiles:
      projectiles.remove(projectile)

    time = pygame.time.get_ticks()

    remove_guests = []
    for guest in guests:
      guest.y += guest.dy
      if guest.y > WINDOW_HEIGHT + GUEST_HEIGHT:  # hit bottom of screen
        remove_guests.append(guest)
    for guest in remove_guests:
      guests.remove(guest)

    time_since_last_guest : int = time - last_time_new_guest_visits
    if time_since_last_guest > AFTER_WHAT_TIME_NEW_GUEST_VISITS:
      guests.append(Guest(random.randint(BORDERS, WINDOW_WIDTH-BORDERS-GUEST_WIDTH), 0, 1))
      last_time_new_guest_visits = time

    # draw

    for guest in guests:
      pygame.draw.rect(
        screen,
        "red",
        (guest.x, guest.y, GUEST_WIDTH, GUEST_HEIGHT)
      )

    pygame.draw.rect(
        screen,
        "blue",
        (player_x, WINDOW_HEIGHT - PLAYER_HEIGHT - GAP_BELOW_PLAYER, PLAYER_WIDTH, PLAYER_HEIGHT)
    )

    pygame.display.update()
