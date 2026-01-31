from ctypes.macholib.dylib import dylib_info

import pygame, sys
from pygame.locals import *
import random

DEBUG: bool = False

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

pygame.init()
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

PLAYER_WIDTH: int = 48
PLAYER_HEIGHT: int = 48
GAP_BELOW_PLAYER: int = 24

player = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT - PLAYER_HEIGHT - GAP_BELOW_PLAYER, PLAYER_WIDTH, PLAYER_HEIGHT)
time = 0
AFTER_WHAT_TIME_NEW_GUEST_VISITS = 3000
BORDERS = 200

last_time_new_guest_visits = 0

projectiles = []
PROJECTILE_WIDTH: int = 48
PROJECTILE_HEIGHT: int = 48
class Projectile:
  def __init__(self, x, y, dy):
    self.rect = pygame.Rect(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
    self.dy = dy


guests = []
GUEST_WIDTH: int = 48
GUEST_HEIGHT: int = 48
class Guest:
  def __init__(self, x, y, dy):
    self.rect = pygame.Rect(x, y, GUEST_WIDTH, GUEST_HEIGHT)
    self.dy = dy


pygame.display.set_caption('Masketeer')
fontObj = pygame.font.Font('freesansbold.ttf', 32)


while True:  # main game loop
    dt = clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # key handling
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player.x -= 10
    if keys[K_RIGHT]:
        player.x += 10
    if keys[K_SPACE]:
        # shoot mask
        if not projectiles:
            projectiles.append(Projectile(player.x, WINDOW_HEIGHT - player.height - GAP_BELOW_PLAYER, -5))


    if player.x < BORDERS:
        player.x = BORDERS

    if player.x >= (max_x := (WINDOW_WIDTH - BORDERS - player.width)):
        player.x = max_x

    pygame.draw.rect(screen, LIGHT_GREY,
                     pygame.Rect(0 + BORDERS, 0, WINDOW_WIDTH - BORDERS - BORDERS, WINDOW_HEIGHT))

    remove_projectiles = []
    for projectile in projectiles:
        projectile.rect.y += projectile.dy
        pygame.draw.rect(screen, "yellow",
                       pygame.Rect(projectile.rect.x, projectile.rect.y, projectile.rect.width, projectile.rect.height))
        if projectile.rect.y < - projectile.rect.height:
            remove_projectiles.append(projectile)
    for projectile in remove_projectiles:
      projectiles.remove(projectile)

    time = pygame.time.get_ticks()

    remove_guests = []
    for guest in guests:
      guest.rect.y += guest.dy
      if guest.rect.y > WINDOW_HEIGHT + guest.rect.height:  # hit bottom of screen
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
        (guest.rect.x, guest.rect.y, guest.rect.width, guest.rect.height)
      )

    pygame.draw.rect(
        screen,
        "blue",
        player
    )

    for projectile in projectiles:
      for guest in guests:
        if projectile.rect.colliderect(guest.rect):
          guests.remove(guest)
          projectiles.remove(projectile)

    for guest in guests:
      if guest.rect.colliderect(player):
        pygame.quit()
        sys.exit()


    pygame.display.update()
