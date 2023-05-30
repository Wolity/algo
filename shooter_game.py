from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_z] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_x] and self.rect.x < win_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('./bullet.png', self.rect.centerx, self.rect.top, 15,20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2 = font.Font(None,36)
font1 = font.Font(None,80)
win = font1.render('VICTORY!', True,(255,255,255))
lose = font1.render('YOU LOSE', True,(180,0,0))

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_monster = 'ufo.png'
life = 3

win_width = 700
win_height = 500
score = 0
lost = 0
goal = 50
max_lost = 25    




display.set_caption('Shooter')
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height-100, 80, 100, 10)


monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_monster, randint(80, win_width -80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('./asteroid.png',randint(30, win_width-30), -40,80,50, randint(1,7))
    asteroids.add(asteroid)
finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
    if not finish:
        window.blit(background, (0,0))
        text = font2.render('Счёт:'+str(score), 1, (255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущено:'+str(lost), 1, (255,255,255))
        window.blit(text_lose,(10,50))
        text_life = font1.render(str(life), 1, (255,0,0))
        window.blit(text_life, (650,10))
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        ship.update()
        asteroids.update()
        ship.reset()

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_monster, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        # if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        #     finish = True
        #     window.blit(lose,(200,200))
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -=1
        if life == 0 or lost>= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        display.update()
    else:
        finish = False
        score = 0 
        lost = 0
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy('./ufo.png',randint(80,win_width-80), -40,80,50, randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy('./asteroid.png', randint(30, win_width-30), -40,80,50, randint(1,7))
            asteroids.add(asteroid)

    time.delay(30)