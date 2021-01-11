import pygame as pg
import random
import os
from os import path

#setup
WIDTH = 800
HEIGHT = 800
FPS = 60
POWERTIME = 5000
HIGH_SCORE = 0
READY = False


playtime = 0.0

# colours
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# folders & Assets

game_folder = os.path.dirname(__file__)
pokemon_art_folder = path.join(game_folder, "Sprite-art", "Pokemon")
star_art = path.join(game_folder, "Sprite-art", "Stars")
white_smoke_art = path.join(game_folder, "Sprite-art", "Smoke", "White puff")
pokemonsound_folder = path.join(game_folder, "Music", "pokemon")
sound_effects = path.join(game_folder, "Music", "Sound Effects")
upgrade_art = path.join(game_folder, "Sprite-art", "Pokemon", "Bolt-Badges")

#Initialize the game
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Gunner")
clock = pg.time.Clock()
mainloop = True
game_over = True

# functions

font_name = pg.font.match_font("Arial")

def draw_text(surf, text, size, x , y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    all_mobs.add(m)

def draw_shieldbar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGTH = 10
    fill = (pct / player1.startshield) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGTH)
    pg.draw.rect(surf, BLUE, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + (25 * i)
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    screen.blit(bonus_images["Shield"], (WIDTH * 0.20, HEIGHT * 0.5))
    screen.blit(bonus_images["Move"], (WIDTH * 0.8, HEIGHT * 0.5))
    draw_text(screen, "Shield Booster", 18, WIDTH * 0.22, HEIGHT * 0.55)
    draw_text(screen, "Move Booster", 18, WIDTH * 0.82, HEIGHT * 0.55)
    draw_text(screen, "Pikafun", 64, WIDTH / 2, HEIGHT * 0.05)
    draw_text(screen, "Arrow keys are for movement, spacebar to fire", 22, WIDTH / 2, HEIGHT * 0.25)
    ready = draw_text(screen, "Press space to begin", 18, WIDTH / 2, HEIGHT * 3/4)
    draw_text(screen, "Current High Score = " + HIGH_SCORE.__str__(), 18, WIDTH / 2, HEIGHT * 0.8)
    pg.display.flip()
    waiting = True
    while waiting:
         clock.tick(FPS)
         for ding in pg.event.get():
             if ding.type == pg.QUIT:
                 pg.quit()
             if ding.type == pg.KEYDOWN:
                 keystate = pg.key.get_pressed()
                 if keystate[pg.K_SPACE]:
                    waiting = False
                    pg.mixer.music.play(loops=-1)


# Classes

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (80,80))
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.speedy = 0
        self.startshield = 45
        self.shield = self.startshield
        self.shoot_delay = 500
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.powerlevel = 1
        self.power_time = pg.time.get_ticks()
        self.spawntime = pg.time.get_ticks()
        self.spawnprotection = 2000


    def update(self):


        if self.powerlevel >= 2 and pg.time.get_ticks() - self.power_time > POWERTIME:
            self.powerlevel -= 1
            self.power_time = pg.time.get_ticks()

        if self.hidden and pg.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.spawntime = pg.time.get_ticks()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        if self.hidden == False:
            keystate = pg.key.get_pressed()
            if keystate [pg.K_LEFT]:
                self.speedx = -10
            if keystate [pg.K_RIGHT]:
                self.speedx = 10
            if keystate [pg.K_UP]:
                self.speedy = -10
            if keystate [pg.K_DOWN]:
                self.speedy = 10
            if keystate [pg.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT


    def powerup(self):
        if self.powerlevel < 2:
            self.powerlevel += 1
        self.power_time = pg.time.get_ticks()


    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.powerlevel == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                pikasound.play()
            elif self.powerlevel >= 2:
                bullet = Bullet(self.rect.left + 20, self.rect.top)
                bullet2 = Bullet(self.rect.right - 20, self.rect.top)
                all_sprites.add(bullet)
                all_sprites.add(bullet2)
                bullets.add(bullet)
                bullets.add(bullet2)
                pikasound.play()


    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        player1.lives -= 1
        player1.shield = player1.startshield
        player1.powerlevel = 1

class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        pokechoice = random.choice(mob_images)
        pokeball = (mob_images.index(pokechoice))
        self.image_orig = pg.transform.scale(pokechoice, (20,20))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width /2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 8)
        self.speedx = random.randrange(-1,2)
        self.value = 0
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()
        if pokeball == 0:
            self.value = 1
        elif pokeball == 1:
            self.value = 2
        elif pokeball == 2:
            self.value = 3
        else:
            self.value = 5

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot +self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT +10 or self.rect.left < -20 or self.rect.right > WIDTH +20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)




class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(bullet_img, (30,30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -12

    def update(self):
        self.rect.y += self.speedy
        # delete bullets after going off-screen
        if self.rect.bottom < 0:
            self.kill()

class Bonus(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(["Shield", "Move"])
        self.image = bonus_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # delete bullets after going off-screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class Starburst(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = broken_pokeballs[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 40


    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(broken_pokeballs[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = broken_pokeballs[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




#Graphics
background = pg.image.load(path.join(pokemon_art_folder, "simple.jpg")).convert_alpha()
background = pg.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

player_img = pg.image.load(path.join(pokemon_art_folder, "pika.png")).convert_alpha()
player_life = pg.transform.scale(player_img, (20, 20))
#mob_img = pg.image.load(path.join(pokemon_art_folder, "pokeball.png")).convert_alpha()
bullet_img = pg.image.load(path.join(pokemon_art_folder, "bolt.png")).convert_alpha()

mob_images = []
mobs = ["pokeball.png", "greatball.png", "Ultraball.png", "masterball.png"]

for img in mobs:
    mob_images.append(pg.image.load(path.join(pokemon_art_folder, img)).convert_alpha())

broken_pokeballs = {}
broken_pokeballs["lg"] = []
broken_pokeballs["sm"] = []
broken_pokeballs["capture"] = []

for star in range(1, 5):
    filename = "Stars_01_128x128_00{}.png".format(star)
    starimage = pg.image.load(path.join(star_art, filename)).convert_alpha()
    starimage_large = pg.transform.scale(starimage, (20, 20))
    broken_pokeballs["lg"].append(starimage_large)
    starimage_small = pg.transform.scale(starimage, (10, 10))
    broken_pokeballs["sm"].append(starimage_small)

    filename = "whitePuff0{}.png".format(star)
    puff = pg.image.load(path.join(white_smoke_art, filename)).convert_alpha()
    puff = pg.transform.scale(puff, (40, 40))
    broken_pokeballs["capture"].append(puff)

bonus_images = {}
bonus_images["Shield"] = pg.transform.scale(pg.image.load(path.join(
    upgrade_art, "bolt-icon-button-blue.png")).convert_alpha(),(30,30))
bonus_images["Move"] = pg.transform.scale(pg.image.load(path.join(
    upgrade_art, "bolt-icon-button-red.png")).convert_alpha(),(30,30))



# sounds

pikasound = pg.mixer.Sound(path.join(pokemonsound_folder, "pikapi.wav"))
pg.mixer.music.load(path.join(pokemonsound_folder, "route1.wav"))
pg.mixer.music.set_volume(0.25)

capturesound = pg.mixer.Sound(path.join(pokemonsound_folder, "pika.wav"))

powerupsound = pg.mixer.Sound(path.join(sound_effects, "powerup.wav"))
powerupsound.set_volume(0.50)







#The game loop

while mainloop:
    if game_over:
        show_go_screen()
        game_over = False

        # spritegroup
        all_sprites = pg.sprite.Group()
        all_mobs = pg.sprite.Group()
        bullets = pg.sprite.Group()
        bonus = pg.sprite.Group()

        # sprites
        player1 = Player()
        all_sprites.add(player1)

        for i in range(30):
            newmob()

        # variables
        score = 0




    #if player1.shield <= player1.startshield:
        #player1.shield += 0.05

    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            mainloop = False # pg window closed by user

    # update sprites
    all_sprites.update()

    # Collision Check player-mobs
    enemyhits = pg.sprite.spritecollide(player1, all_mobs, True, pg.sprite.collide_circle)
    for hit in enemyhits:

        if pg.time.get_ticks() - player1.spawntime > player1.spawnprotection:
            player1.shield -= hit.value * 10
        newmob()
        if player1.shield <= 0:
            capture_poof = Starburst(player1.rect.center, "capture")
            all_sprites.add(capture_poof)
            capturesound.play()
            player1.hide()



    # Collision Check bullets
    bullet_hits = pg.sprite.groupcollide(all_mobs, bullets, True, True)
    for hit in bullet_hits:
        score += hit.value
        cracked = Starburst(hit.rect.center, "lg")
        all_sprites.add(cracked)
        if random.random() > 0.9:
            bon = Bonus(hit.rect.center)
            all_sprites.add(bon)
            bonus.add(bon)
        newmob()

    # Collision Check bonus
    hits = pg.sprite.spritecollide(player1, bonus, True)
    for hit in hits:
        powerupsound.play()
        if hit.type == "Shield":
            player1.shield += 10
            if player1.shield > player1.startshield:
                player1.shield = player1.startshield
        if hit.type == "Move":
            player1.powerup()

    if player1.lives == 0 and not capture_poof.alive():
        game_over = True
        pg.mixer.music.stop()
        if score > HIGH_SCORE:
            HIGH_SCORE = score

    # draw the sprites
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH - 30, HEIGHT - 30)
    draw_shieldbar(screen, 5, HEIGHT - 20, player1.shield)
    draw_lives(screen, 10, HEIGHT - 50, player1.lives, player_life)


    # create the display
    pg.display.flip()  # flip the screen 60 times a second

    # ------- draw pattern ------------------

print ("This 'game' was played for %.2f seconds." % playtime)