
from pygame import *
from random import randint
from time import time as timer
font.init()
lost = 0 
score = 0
live = 3
w = display.set_mode((700, 500))
display.set_caption('Шутер')
bg = transform.scale(image.load('pngwing.com (4).png'), (700, 500))


mixer.init()
mixer.music.load('Galactic Rap.mp3')
mixer.music.play()
mixer.music.set_volume(0.07)

class GameSpr(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        w.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSpr):
    def update(self):
        key_p = key.get_pressed()
        if key_p[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_p[K_d] and self.rect.x < 610:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 21, 17, 9)
        bullets.add(bullet)

class Enemy(GameSpr):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 700:
            self.rect.x = randint(60, 450)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSpr):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

            
            
            


font.init()
font1 = font.SysFont('Comic Sans MS', 70)
win = font1.render('You Win', True, (0, 255, 0))
lose = font1.render('You Lose', True, (255, 0, 0))
hero = Player('pngwing.com (5).png', 320, 400, 95, 100, 4)
font2 = font.SysFont('Comic Sans MS', 30)
font3 = font.SysFont('Comic Sans MS', 50)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('pngwing.com (6).png', randint(60, 450), -40, 80, 50, randint(1, 2))
    monsters.add(monster)



bullet = sprite.Group()


asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('pngwing.com (1).png', randint(60, 450), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()


rel_time = False
num_fire = 0


fire = mixer.Sound('fire.ogg')


game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire.play()
                    hero.fire()
                    num_fire += 1
    
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
                
    
    
    if not finish:
        w.blit(bg, (0,0))

    
    
        

        text_lost = font2.render('Пропушено: ' + str(lost), 1, (255, 255, 255))
        text_score = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        text_live = font3.render('HP ' + str(live), 1, (255, 255, 255))

        if sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            monster = Enemy('pngwing.com (6).png', randint(60, 450), -40, 80, 50, randint(1, 2))
            monsters.add(monster)

        if sprite.groupcollide(asteroids, bullets, True, True):
            asteroid = Enemy('pngwing.com (1).png', randint(60, 450), -40, 80, 50, randint(1, 3))
            asteroids.add(asteroid)


        if score > 14:
            w.blit(win, (200, 200))
            finish = True

        if sprite.spritecollide(hero, monsters, False):
            w.blit(lose, (200, 200))
            finish = True

        if sprite.spritecollide(hero, asteroids, True):
            live -= 1
    

        if live == 0:
            w.blit(lose, (200, 200))
            finish = True
            

        hero.reset()
        hero.update()    
        monsters.draw(w)
        monsters.update()
        asteroids.draw(w)
        asteroids.update()
        bullets.draw(w)
        bullets.update()
        w.blit(text_lost, (10, 20))
        w.blit(text_score, (10, 50))
        w.blit(text_live, (560, 20))

        if rel_time:
            now_time = timer()
            if now_time - last_time < 2:
                reloud = font2.render('Перезарятка ', True, (150, 0, 0))
                w.blit(reloud, (250, 400))
            else:
                num_fire = 0
                rel_time = False
    display.update()
    time.delay(10)
