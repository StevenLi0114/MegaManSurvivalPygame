import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk1 = pygame.image.load('graphics/megamanwalk1.png').convert_alpha()
        self.player_walk2 = pygame.image.load('graphics/megamanwalk2.png').convert_alpha()
        self.player_walk3 = pygame.image.load('graphics/megamanwalk3.png').convert_alpha()
        self.players = [self.player_walk1, self.player_walk2, self.player_walk3]
        self.player_idx = 0
        self.player_jump = pygame.image.load('graphics/megamanjump.png').convert_alpha()
        self.image = self.players[self.player_idx]
        self.rect = self.image.get_rect(topleft=(10, 350))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("graphics/cartoonjump.mp3")
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.top >= 350:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.top >= 350:
            self.rect.top = 350

    def animation_state(self):
        if self.rect.top < 350:
            self.image = self.player_jump
        else:
            self.player_idx += 0.1
            if self.player_idx >= len(self.players):
                self.player_idx = 0
            self.image = self.players[int(self.player_idx)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "wasp":
            wasp_1 = pygame.image.load('graphics/wasp1.png').convert_alpha()
            wasp_2 = pygame.image.load('graphics/wasp2.png').convert_alpha()
            self.frames = [wasp_1, wasp_2]
            y_pos = 270
        else:
            turtle_1 = pygame.image.load('graphics/turtle1.png').convert_alpha()
            turtle_2 = pygame.image.load('graphics/turtle2.png').convert_alpha()
            turtle_3 = pygame.image.load('graphics/turtle3.png').convert_alpha()
            self.frames = [turtle_1, turtle_2, turtle_3]
            y_pos = 370
        self.animation_idx = 0
        self.image = self.frames[self.animation_idx]
        if self.animation_idx == 0 and type != "wasp":
            y_pos = 370
        self.rect = self.image.get_rect(topleft=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_idx += 0.1
        if self.animation_idx >= len(self.frames):
            self.animation_idx = 0
        self.image = self.frames[int(self.animation_idx)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coin0 = pygame.image.load("graphics/coin0.png")
        coin1 = pygame.image.load("graphics/coin1.png")
        coin2 = pygame.image.load("graphics/coin2.png")
        coin3 = pygame.image.load("graphics/coin3.png")
        coin4 = pygame.image.load("graphics/coin4.png")
        coin5 = pygame.image.load("graphics/coin5.png")
        coin6 = pygame.image.load("graphics/coin6.png")
        coin7 = pygame.image.load("graphics/coin7.png")
        self.animation_idx = 0
        self.frames = [coin0, coin1, coin2, coin3, coin4, coin5, coin6, coin7]
        self.image = self.frames[self.animation_idx]
        self.rect = self.image.get_rect(topleft=(randint(900, 1100), 240))

    def animation_state(self):
        self.animation_idx += 0.1
        if self.animation_idx >= len(self.frames):
            self.animation_idx = 0
        self.image = self.frames[int(self.animation_idx)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_time():
    curr_time = (pygame.time.get_ticks() - start_time) // 1000
    if curr_time >= 60:
        minutes = curr_time // 60
        seconds = curr_time - minutes * 60
        if seconds < 10:
            time_display = str(minutes) + ":" + "0" + str(seconds)
        else:
            time_display = str(minutes) + ":" + str(seconds)
    else:
        time_display = str(curr_time)
    time_surface = test_font.render("Time: " + time_display, False, (64, 64, 64))
    time_rect = time_surface.get_rect(center=(200, 50))
    screen.blit(time_surface, time_rect)
    return curr_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def coin_collision():
    global score
    if pygame.sprite.spritecollide(player.sprite, coin, True):
        score += 1
        coin_sound = pygame.mixer.Sound("graphics/collectcoin.mp3")
        coin_sound.set_volume(0.1)
        coin_sound.play()

def display_score():
    score_surface = test_font.render("Score: " + str(score), False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(600, 50))
    screen.blit(score_surface, score_rect)

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Mega Man's Survival")
clock = pygame.time.Clock()
test_font = pygame.font.Font('graphics/NaFont.ttf', 50)
screen.fill('white')
game_active = False
sky = pygame.image.load('graphics/sky.jpg').convert_alpha()
ground = pygame.image.load('graphics/ground.png').convert_alpha()
start_time = 0

game_name = test_font.render("Mega Man's Survival", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_instruct = test_font.render("Press space to run!", False, (111, 196, 169))
game_instruct_rect = game_instruct.get_rect(center=(400, 350))
time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

coin = pygame.sprite.Group()

bg_music = pygame.mixer.Sound("graphics/pixelplains.mp3")
bg_music.set_volume(0.01)
bg_music.play(loops=-1)
# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 5000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['wasp', 'turtle', 'turtle'])))
            if event.type == coin_timer:
                coin.add(Coin())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score = 0
                start_time = pygame.time.get_ticks()
    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 0))
        time = display_time()
        display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        coin.draw(screen)
        coin.update()
        coin_collision()
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 164))
        end_surf = pygame.transform.rotozoom(Player().image, 0, 2)
        end_rect = end_surf.get_rect(center=(400, 250))
        score_message = test_font.render(f'Final Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 300))
        time_message = test_font.render(f'Your Time: {time}', False, (111, 196, 169))
        time_message_rect = time_message.get_rect(center=(400, 200))
        screen.blit(game_name, game_name_rect)
        objective_message = test_font.render("Objective: Survive as long as possible!", False, (111, 196, 169))
        objective_message_rect = objective_message.get_rect(center=(400, 430))
        if time == 0:
            screen.blit(game_instruct, game_instruct_rect)
            screen.blit(objective_message, objective_message_rect)
            screen.blit(end_surf, end_rect)
        else:
            screen.blit(time_message, time_message_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
