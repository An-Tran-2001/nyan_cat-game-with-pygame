import pygame
import os
import random
pygame.init()
width = 800
height = 400
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Game nyan Cat')
clock = pygame.time.Clock()
FPS = 60
BLUE = (141, 238, 238)
RED = (255, 0, 0)
score_font = pygame.font.SysFont('comicsans', 15)


class Load_image():
    def __init__(self, folder, name_image_file, total_files, scale):
        self.image_list = []
        for i in range(total_files):
            self.name_image_file = name_image_file
            self.name_image_file = self.name_image_file + \
                ' (' + str(i+1) + ')' + '.png'
            self.image = pygame.image.load(
                os.path.join(folder, self.name_image_file))
            self.image = pygame.transform.scale(
                self.image, (self.image.get_width()//scale, self.image.get_height()//scale))
            self.image_list.append(self.image)


class Common_object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Cat(Common_object):
    def __init__(self, x, y, image, rainbow):
        super().__init__(x, y, 0, 0, image)
        self.rainbow_list = rainbow
        self.image_list = image
        self.image_cat = image[0]
        self.cat_rect = image[0].get_rect()
        self.cat_rect.center = (x, y)
        self.rainbow = rainbow[0]
        self.rainbow_rect = self.rainbow.get_rect()
        self.frames_count_cat = 0
        self.frames_count_rainbow = 0
        self.gravity = 30
        self.jump_height = self.gravity
        self.jump = False

    def run_animation(self):
        if self.frames_count_cat // 5 >= len(self.image_list):
            self.frames_count_cat = 0
        self.image_cat = self.image_list[self.frames_count_cat //
                                         5]
        self.frames_count_cat += 1

    def rainbow_animation(self):
        if self.frames_count_rainbow // int(FPS * 10 / 100) >= len(self.rainbow_list):
            self.frames_count_rainbow = 0
        self.rainbow = self.rainbow_list[self.frames_count_rainbow //
                                         int(FPS * 10 / 100)]

        self.frames_count_rainbow += 1

    def draw_fly(self):
        self.run_animation()
        self.rainbow_animation()
        screen.blit(self.rainbow, (self.cat_rect.x - self.image_cat.get_width() /
                    2, self.cat_rect.y - self.image_cat.get_height()/2))
        screen.blit(self.rainbow, (self.cat_rect.x - self.image_cat.get_width() / 2 - self.rainbow.get_width() /
                    2, self.cat_rect.y - self.image_cat.get_height()/2))
        screen.blit(self.image_cat, (self.cat_rect))

    def draw_walk(self):
        self.run_animation()
        screen.blit(self.image_cat, (self.cat_rect))

    def cat_jump(self):
        if self.jump_height >= -self.gravity:
            neg = 1
            if self.jump_height < 0:
                neg = -1
            self.cat_rect.y -= int((self.jump_height ** 2) * 0.025 * neg)
            self.jump_height -= 1
        else:
            self.jump = False
            self.jump_height = self.gravity

    def move(self):
        if self.jump == False:
            self.draw_fly()
        else:
            self.cat_jump()
            self.draw_fly()
            # screen.blit(self.image_cat, (self.cat_rect))

    def collide(self, other):
        return self.cat_rect.colliderect(other.rect)


class Background(Common_object):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image)
        self.image_list = image
        self.speed = speed
        self.image = pygame.transform.scale(image[0], (width, height))
        self.rect = self.image.get_rect()
        self.frame_count = 0

    def animation(self):
        if self.frame_count // 5 < len(self.image_list) - 1:
            self.frame_count += 1
            self.image = self.image = pygame.transform.scale(
                self.image_list[self.frame_count // 5], (width, height))
        else:
            self.frame_count = 0

    def reset_background(self):
        Common_object.draw(self)
        screen.blit(self.image, (self.x + self.width, self.y))
        self.x -= self.speed
        if self.x < -self.width:
            self.x = 0

    def draw(self):
        self.animation()
        self.reset_background()


class Floor(Common_object):
    def __init__(self, x, y, width, height, speed):
        Common_object.__init__(self, x, y, width, height, None)
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join('assets/floor', 'floor.png')), (width, 25))

    def draw(self):
        Background.reset_background(self)


class BonggoCat(Common_object):
    def __init__(self, x, y, image):
        super().__init__(x, y, 0, 0, image)
        self.image_list = image
        self.border = pygame.transform.scale(pygame.image.load(
            os.path.join('assets/bongo cat', 'border.png')), (image[0].get_width() + 30, image[0].get_height()+70))
        self.check_input = False

    def draw(self):
        if self.check_input == True:
            self.image = self.image_list[1]
        else:
            self.image = self.image_list[0]
        screen.blit(self.image, (self.x+17, self.y+20))
        screen.blit(self.border, (self.x, self.y-13))


class Enemy(Common_object):
    def __init__(self, x, y, image, speed, flip):
        super().__init__(x, y, 0, 0, image)
        self.image_list = image
        self.speed = speed + 1
        self.frames_count = 0
        self.rect = self.image[0].get_rect()
        self.rect.center = (x, y)
        self.flip = flip

    def animation(self):
        if self.frames_count // 5 >= len(self.image_list):
            self.frames_count = 0
        self.image = self.image_list[self.frames_count // 5]
        self.frames_count += 1

    def run(self):
        self.rect.x -= self.speed

    def draw(self):
        self.animation()
        self.run()
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


class Dict_enemy():
    def __init__(self, dict_enemy, cat):
        self.dict_enemy = dict_enemy
        self.cat = cat

    def draw_and_collision(self, check_die):
        for key, value in self.dict_enemy.items():
            for enemy in value:
                enemy.draw()
                if enemy.rect.x < -enemy.image.get_width():
                    value.remove(enemy)
                if self.cat.collide(enemy):
                    check_die = True
                # pygame.draw.rect(screen, RED, enemy.rect, 2)
        return check_die


class Play_game():
    def __init__(self):
        self.jazz = Load_image('assets/jazz_cat', 'jazz', 12, 4)
        self.rainbow = Load_image('assets/rainbow', 'rainbow', 4, 12)
        self.player1 = Cat(100, 350, self.jazz.image_list,
                           self.rainbow.image_list)
        self.image_enemy = Load_image('assets/hehe', 'hehe', 7, 5)
        #
        self.background = Load_image('assets/background', 'background', 6, 1)
        self.bongo_cat = Load_image('assets/bongo cat', 'bongo_cat', 2, 6)

        self.background_obj = Background(
            0, 0, width, height, self.background.image_list, 2)
        self.bongocat = BonggoCat(0, 0, self.bongo_cat.image_list)
        #
        self.floor = Floor(0, height - 28,  width, height, 2)
        #
        self.stone_img = Load_image('assets/stone', 'stone', 1, 20)
        #
        self.score = 0
        self.height_score = 0
        #
        self.stone_list = []
        self.enemy_list = []
        self.frames_count = 0
        self.die = False

    def add_stone(self):
        self.frames_count += 1
        if self.frames_count % 100 == 0:
            self.enemy_list.append(Enemy(random.randint(
                width, width+100), height - 40, self.image_enemy.image_list, 4, True))
        if self.score % 100 == 0 and self.score != 0 and self.stone_list == []:
            self.stone_list.append(Enemy(width, random.randint(
                200, 270), self.stone_img.image_list, 2, False))
        dict_enemy = {"walk": self.enemy_list, "fly": self.stone_list}
        if self.frames_count % 10 == 0:
            self.score += 1
        self.dict_enemy = Dict_enemy(dict_enemy, self.player1)

    def draw(self):
        self.add_stone()
        self.background_obj.draw()
        self.bongocat.draw()
        self.player1.move()
        self.die = self.dict_enemy.draw_and_collision(self.die)
        screen.blit(score_font.render(
            f"Height Score: {self.height_score}  ||  Score: {self.score}", 2, (255, 255, 255)), (width - 240, 10))

        self.floor.draw()

    def run(self):
        self.draw()

    def remove(self):
        self.enemy_list = []
        self.stone_list = []
        self.frames_count = 0
        self.score = 0


def main():
    start_game = Play_game()
    while True:
        while start_game.die == False:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        start_game.player1.jump = True
                        start_game.bongocat.check_input = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        start_game.bongocat.check_input = False
            start_game.run()
            pygame.display.update()
        if start_game.height_score < start_game.score:
            screen.blit(score_font.render(
                f"Hight score : {start_game.score}", 2, (255, 255, 255)), (width / 2 - 50, height/2 - 25))
        screen.blit(score_font.render("Please press space to play again",
                    2, (255, 255, 255)), (width / 2 - 100, height/2))

        if start_game.die == True and start_game.height_score < start_game.score:
            start_game.height_score = start_game.score

        # pygame.draw.rect(screen, RED, start_game.player1.cat_rect, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game.die = False
                    start_game.remove()
        pygame.display.update()


if __name__ == '__main__':
    main()
