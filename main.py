import pygame, sys
from pygame.locals import *
import random

DEBUG: bool = False
pygame.mixer.init(frequency=16000)
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play()

fx_shoot = pygame.mixer.Sound("shoot.mp3")
fx_social_distance = pygame.mixer.Sound("Pass social Distance.mp3")
fx_cough = pygame.mixer.Sound("cough.mp3")
fx_sneeze = pygame.mixer.Sound("sneeze.mp3")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

pygame.init()
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BORDERS = 200
SOCIAL_DISTANCE = 450
DISTANCE_BOX = pygame.Rect(BORDERS, SOCIAL_DISTANCE, WINDOW_WIDTH - BORDERS * 2, 4)

PLAYER_WIDTH: int = 48
PLAYER_HEIGHT: int = 48
GAP_BELOW_PLAYER: int = 24

player = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT - PLAYER_HEIGHT - GAP_BELOW_PLAYER, PLAYER_WIDTH, PLAYER_HEIGHT)
player_health = 300
time = 0
AFTER_WHAT_TIME_NEW_GUEST_VISITS = 3000
score = 0
game_start_time = 0 # start time is set on game start


PLAYER_IMAGE_WITHOUT_FIRE_UNSCALED = pygame.image.load("without_fire.png")
PLAYER_IMAGE_WITHOUT_FIRE = pygame.transform.scale(PLAYER_IMAGE_WITHOUT_FIRE_UNSCALED, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))

PLAYER_IMAGE_WITH_FIRE_UNSCALED = pygame.image.load("with_fire_1.png")
PLAYER_IMAGE_WITH_FIRE = pygame.transform.scale(PLAYER_IMAGE_WITH_FIRE_UNSCALED, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))


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
        self.state = "without_mask"

MASK_UNSCALED = pygame.image.load("mask.png")
MASK_SCALED = pygame.transform.scale(MASK_UNSCALED, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))


GUEST_IMAGE_UNSCALED = pygame.image.load("without_mask.png")
GUEST_IMAGE = pygame.transform.scale(GUEST_IMAGE_UNSCALED, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))

GUEST_IMAGE_WITH_MASK_UNSCALED = pygame.image.load("with_mask.png")
GUEST_IMAGE_WITH_MASK = pygame.transform.scale(GUEST_IMAGE_WITH_MASK_UNSCALED, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))

GUEST_IMAGE_SICK_UNSCALED = pygame.image.load("sick.png")
GUEST_IMAGE_SICK= pygame.transform.scale(GUEST_IMAGE_SICK_UNSCALED, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))

SUPPLIER_WIDTH: int = 48
SUPPLIER_HEIGHT: int = 48
class Supplier:
    def __init__(self, x, y, dy):
        self.rect = pygame.Rect(x, y, SUPPLIER_WIDTH, SUPPLIER_HEIGHT)
        self.dy = dy
suppliers : list[Supplier] = []


MASK_BOX_UNSCALED = pygame.image.load("mask_box.png")
MASK_BOX_SCALED = pygame.transform.scale(MASK_BOX_UNSCALED, (SUPPLIER_WIDTH * 2, SUPPLIER_HEIGHT * 2))

VACCINE_WIDTH: int = 48
VACCINE_HEIGHT: int = 48
class Vaccine:
    def __init__(self, x, y, dy):
        self.rect = pygame.Rect(x, y, VACCINE_WIDTH, VACCINE_HEIGHT)
        self.dy = dy

VACCINE_IMAGE_UNSCALED = pygame.image.load("vaccine.png")
VACCINE_IMAGE = pygame.transform.scale(VACCINE_IMAGE_UNSCALED, (VACCINE_WIDTH * 2, VACCINE_HEIGHT * 2))
vaccines : list[Vaccine] = []

AFTER_WHAT_TIME_A_NEW_VACCINE_COMES = 40000
last_time_new_vaccine_came = 0

PAUSE_IMAGE_UNSCALED = pygame.image.load("game paused.png")
PAUSE_IMAGE = pygame.transform.scale(PAUSE_IMAGE_UNSCALED, (800, 600))


START_IMAGE_UNSCALED = pygame.image.load("instructions.png")
START_IMAGE = pygame.transform.scale(START_IMAGE_UNSCALED, (800, 600))

pygame.display.set_caption('Masketeer')
fontObj = pygame.font.Font('freesansbold.ttf', 24)

mask_count: int = 10

global scene
scene = 'start'

def start():
    global scene, score, player_health, last_time_new_guest_visits, last_time_new_vaccine_came, mask_count, game_start_time
    # handle events (also listen for keydown to reliably catch presses)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                # reset game state and switch to game scene
                score = 0
                player_health = 300
                game_start_time = pygame.time.get_ticks()
                last_time_new_guest_visits = 0
                last_time_new_vaccine_came = 0
                mask_count = 10
                guests.clear()
                projectiles.clear()
                suppliers.clear()
                vaccines.clear()
                scene = 'game'
                return

    # draw a simple start screen so players know to press SPACE
    screen.blit(START_IMAGE, (0, 0))

    pygame.display.update()
    clock.tick(60)
        

def game():
    dt = clock.tick(60)
    global score, player_health, last_time_new_guest_visits, last_time_new_vaccine_came, mask_count, scene
    score = score + 1

    if player_health <= 0:
        print (f"Your score was {score}!")
        pygame.quit()
        sys.exit()

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
        if not projectiles and mask_count > 0:
            mask_count = mask_count - 1
            projectiles.append(Projectile(player.x, WINDOW_HEIGHT - player.height - GAP_BELOW_PLAYER, -5))
            pygame.mixer.Sound.play(fx_shoot)
            if mask_count <= 2:
                suppliers.append(Supplier(player.x, -SUPPLIER_HEIGHT, 3))

    if keys[K_ESCAPE]:
        scene = 'pause'
        return
    
    if player.x < BORDERS:
        player.x = BORDERS

    if player.x >= (max_x := (WINDOW_WIDTH - BORDERS - player.width)):
        player.x = max_x

    pygame.draw.rect(screen, BLACK,
                     pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.draw.rect(screen, DARK_GREY,
                     pygame.Rect(0 + BORDERS, 0, WINDOW_WIDTH - BORDERS - BORDERS, WINDOW_HEIGHT))

    remove_projectiles = []
    for projectile in projectiles:
        projectile.rect.y += projectile.dy
        screen.blit(MASK_SCALED, (projectile.rect.x - (PROJECTILE_WIDTH/2),
                                  projectile.rect.y - (PROJECTILE_HEIGHT/2)
                                  ))
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

    time_since_last_guest: int = time - last_time_new_guest_visits
    if time_since_last_guest > AFTER_WHAT_TIME_NEW_GUEST_VISITS:
        guests.append(Guest(random.randint(BORDERS, WINDOW_WIDTH - BORDERS - GUEST_WIDTH), 0, 1))
        last_time_new_guest_visits = time
        random_symptom = random.randint(0, 100)
        if random_symptom > 80:
            pygame.mixer.Sound.play(fx_cough)
        elif random_symptom >  60:
            pygame.mixer.Sound.play(fx_sneeze)


    time_since_last_vaccine: int = time - last_time_new_vaccine_came
    if time_since_last_vaccine > AFTER_WHAT_TIME_A_NEW_VACCINE_COMES:
        vaccines.append(Vaccine(random.randint(BORDERS, WINDOW_WIDTH - BORDERS - GUEST_WIDTH), 0, 1))
        last_time_new_vaccine_came = time

    # draw
    pygame.draw.rect(screen, "red", DISTANCE_BOX)

    for supplier in suppliers:
        screen.blit(MASK_BOX_SCALED, (supplier.rect.x - SUPPLIER_WIDTH / 2, supplier.rect.y - SUPPLIER_HEIGHT / 2))

    for vaccine in vaccines:
        screen.blit(VACCINE_IMAGE, (vaccine.rect.x - VACCINE_WIDTH / 2, vaccine.rect.y - VACCINE_HEIGHT / 2))

    for guest in  guests:
        if guest.state == "without_mask":
            screen.blit(GUEST_IMAGE, (guest.rect.x - GUEST_WIDTH / 2, guest.rect.y - GUEST_HEIGHT / 2))
        if guest.state == "with_mask":
            screen.blit(GUEST_IMAGE_WITH_MASK, (guest.rect.x - GUEST_WIDTH / 2, guest.rect.y - GUEST_HEIGHT / 2))
        if guest.state == "sick":
            screen.blit(GUEST_IMAGE_SICK, (guest.rect.x - GUEST_WIDTH / 2, guest.rect.y - GUEST_HEIGHT / 2))

    if not projectiles:
        screen.blit(PLAYER_IMAGE_WITHOUT_FIRE,(player.x - PLAYER_WIDTH / 2, player.y - PLAYER_HEIGHT / 2))
    else:
        screen.blit(PLAYER_IMAGE_WITH_FIRE, (player.x - PLAYER_WIDTH / 2, player.y - PLAYER_HEIGHT / 2))

    for projectile in projectiles:
        for guest in guests:
            if projectile.rect.colliderect(guest.rect):
                guest.state = "with_mask"
                projectiles.remove(projectile)

    for guest in guests:
        if guest.rect.colliderect(DISTANCE_BOX):
            if guest.state == "without_mask":
                guest.state = "sick"
                player_health -= 25
                pygame.mixer.Sound.play(fx_social_distance)

    for supplier in suppliers:
        supplier.rect.y += supplier.dy
        if supplier.rect.colliderect(player):
            # player has picked up mask box
            mask_count = mask_count + 10
            suppliers.remove(supplier)

    for vaccine in vaccines:
        vaccine.rect.y += vaccine.dy
        if vaccine.rect.colliderect(player):
            player_health += 200
            vaccines.remove(vaccine)

    # render HUD
    text_surface = fontObj.render(
        f"Masks: {mask_count}",
        True,  # antialias
        (255, 255, 255)  # text color
    )
    screen.blit(text_surface, (10, 20))

    health_surface = fontObj.render(
        f"Health: {player_health}",
        True,  # antialias
        (255, 255, 255)  # text color
    )
    screen.blit(health_surface, (10, 60))

    score_surface = fontObj.render(
        f"Score: {score:,}",
        True,  # antialias
        (255, 255, 255)  # text color
    )
    screen.blit(score_surface, (10, 100))

    time_surface = fontObj.render(
        f"Time: {(time - game_start_time) // 1_000}",
        True,  # antialias
        (255, 255, 255)  # text color
    )
    screen.blit(time_surface, (10, 140))

    pygame.display.update()

def pause():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                global scene
                scene = 'game'

    # draw a simple pause screen so players know to press ESCAPE to resume
 

    screen.blit(PAUSE_IMAGE, (WINDOW_WIDTH // 2 - PAUSE_IMAGE.get_width() // 2,
                              WINDOW_HEIGHT // 2 - PAUSE_IMAGE.get_height() // 2))

    instr_surface = fontObj.render('Press ESCAPE to resume', True, BLACK)
    screen.blit(instr_surface, (WINDOW_WIDTH // 2 - instr_surface.get_width() // 2, 400))    
    pygame.display.update()
    clock.tick(60)
    

def main():
    global scene
    scene = 'start'
    while True:  # main game loop
        if scene == 'start':
            start()
        elif scene == 'game':
            game()
        elif scene == 'game_over':
            pass
        elif scene == 'pause':
            pause()
    

main()