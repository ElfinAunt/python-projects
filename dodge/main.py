"""
date : 23-1-24
project : a simple car game with python
dev : ElfinAunt
V1 - Completed On : 11-2-24
TOTAL TIME TAKE : 19 Days
"""
import random
import pygame, os

pygame.init()
width = 900
height = 600
root_screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Dodge")
running = True
gameover = False
# lanes
lanes = [(69, 430), (162, 430), (369, 430), (462, 430), (669, 430), (762, 430)]
current_lane = 0
# Player
# player_image = pygame.image.load("E:\\Python Projects\\dodge\\player_vehicles\\Biker.png")
player_image = pygame.image.load("player_vehicles\\Biker.png")
player_vehicles = os.listdir("player_vehicles")

# Enemies
enemy_Xpos = [69, 162, 369, 462, 669, 762]
enemies = []
enemies_images = os.listdir("enemy vehicles")
enemy_selected_vehicles = []


# Music
def main_music():
    pygame.mixer.music.load("sound_tracks\\background_music.mp3")
    pygame.mixer.music.play(1)


main_music()


def crash_sound(sound_type):
    if sound_type == "front":
        pygame.mixer.music.load("sound_tracks\\crash.wav")
        pygame.mixer.music.play()


# Start Screen
game_begin = 0
vehicle_number = 0


def start_screen(vehicle_num):
    global player_image, player_vehicles
    start_screen_img = pygame.image.load("other_images\\start_screen.png")
    root_screen.blit(start_screen_img, (0, 0))
    if len(player_vehicles) > vehicle_num:
        player_image = pygame.image.load(f"player_vehicles\\{player_vehicles[vehicle_number]}")
        root_screen.blit(pygame.transform.rotate(player_image, 270), (width / 2 - 80, 490))


# Score
player_score = 0
font = pygame.font.Font('freesansbold.ttf', 30)


def enemy_spawner(player_pos, player_size):
    global enemies, running, gameover, player_score
    enemy_Ypos = [-200]
    enemy_speed = 5
    while len(enemies) < 5:
        random_x_index = random.choice(enemy_Xpos)
        enemy_vehicle_img = random.choice(enemies_images)
        for enemy in enemies:
            if random_x_index in enemy:
                if (enemy[1] - enemy_Ypos[0]) < 145:
                    enemy_Ypos[0] -= random.randint(200, 250)
        enemies.append([random_x_index, enemy_Ypos[0], 50, 100, enemy_vehicle_img])
    for enemy in enemies:
        enemy[1] += enemy_speed
        enemy_img = pygame.image.load("enemy vehicles\\" + enemy[4])
        root_screen.blit(enemy_img, (enemy[0], enemy[1]))
        if enemy[0] == player_pos[0]:
            if (player_pos[1] - enemy[1]) < (player_size[3]) and enemy[1] < 550:
                if enemy[1] > 400:
                    enemies.remove(enemy)
                    continue
                gameover = True
                crash_sound("front")
                break
        if enemy[1] > height:
            enemies.remove(enemy)
            player_score += 1


# Main Game Screen
def main_handler():
    track_image = pygame.image.load("other_images\\trackone.png").convert()
    track_image = pygame.transform.scale(track_image, (width / 3, height))
    root_screen.blit(track_image, (0, 0))
    root_screen.blit(track_image, (300, 0))
    root_screen.blit(track_image, (600, 0))
    root_screen.blit(player_image, lanes[current_lane])
    if not gameover:
        enemy_spawner(lanes[current_lane], player_image.get_rect())
        text = font.render(f"Score:{player_score}", True, (71, 255, 212), (0, 0, 0))
        textRect = text.get_rect()
        textRect.left = width - textRect.width
        root_screen.blit(text, textRect)
    elif gameover:
        gameover_img = pygame.image.load("other_images\\gameover_screen.jpg").convert()
        root_screen.blit(gameover_img, (0, 125))


# Main Window
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_begin:
                if event.key == pygame.K_RETURN:
                    game_begin = 1
                if event.key == pygame.K_RIGHT and len(player_vehicles) > vehicle_number + 1:
                    vehicle_number += 1
                    start_screen(vehicle_number)
                if event.key == pygame.K_LEFT and vehicle_number - 1 > -1:
                    vehicle_number -= 1
                    start_screen(vehicle_number)

            if gameover:
                if event.key == pygame.K_e:
                    # running = False
                    game_begin = 0
                elif event.key == pygame.K_r:
                    pygame.mixer.music.load("sound_tracks\\background_music.mp3")
                    pygame.mixer.music.play(1)
                    enemies.clear()
                    player_score = 0
                    gameover = False
            if event.key == pygame.K_RIGHT:
                if current_lane >= 5:
                    current_lane -= 6
                current_lane += 1
            if event.key == pygame.K_LEFT:
                if current_lane <= 0:
                    current_lane += 6
                current_lane -= 1
    if not game_begin:
        start_screen(vehicle_number)
    if game_begin:
        main_handler()
    pygame.display.update()
    clock.tick(120)
pygame.quit()
