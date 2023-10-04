#Создай собственный Шутер!
from random import randint
from pygame import *

#окно
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
count1 = 0
count2 = 0

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#классы наследники
class Player(GameSprite):
    def update(self):
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        if keys_pressed[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            mixer.init()
            mixer.music.load('fire.ogg')
            mixer.music.play()


class Enemy(GameSprite):
    def update(self):
        global count2
        if self.rect.y < 500:
            self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 635)
            self.reset()
            count2 += 1

class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y += self.speed
        else:
            self.kill()
        

#спрайты
rocket = Player('rocket.png', 0, 435, 65, 65, 10)

#монстры
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 635), 0, 90, 65, randint(1, 4))
    monsters.add(monster)

#пули
bullets = sprite.Group()


#надпись
font.init()
font = font.Font(None, 20)

win = font.render('ПОБЕДА', True, (255, 255, 255))
lose = font.render('ПОРАЖЕНИЕ', True, (255, 255, 255))
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    keys_pressed = key.get_pressed()

    if finish != True:
        window.blit(background, (0, 0))

        rocket.reset()
        rocket.update()

        monsters.draw(window)
        monsters.update()

        counter = font.render(f'Счёт: {count1}', True, (255, 255, 255))
        mist = font.render(f'Пропущено: {count2}', True, (255, 255, 255))
        window.blit(counter, (0, 0))
        window.blit(mist, (0, 20))

        rocket.fire()
        bullets.draw(window)
        bullets.update()

        if sprite.groupcollide(monsters, bullets, True, True):
            count1 += 1
            monster = Enemy('ufo.png', randint(0, 635), 0, 90, 65, randint(1, 4))
            monsters.add(monster)


        if count1 == 10:
            window.blit(win, (310, 250))
            finish = True


        if sprite.spritecollide(rocket, monsters, False) or count2 >= 3:
            window.blit(lose, (310, 250))
            finish = True
 

    display.update()
    clock.tick(60)