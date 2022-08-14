# 引用函数
import pygame
from random import randrange
from time import sleep
import sys
import os


def source_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


pygame.init()
font = pygame.font.Font(source_path("image/微软雅黑.ttf"), 30)
font.bold = True

# 游戏设置
map_width = 400
map_height = 512
frame = 0
FPS = 165
pipes = [[200, 4]]
bird = [20, 256]
gravity = 0.03
velocity = 0
score = 0


# 设置画布与引用图片
gameScreen = pygame.display.set_mode((map_width, map_height))
clock = pygame.time.Clock()
background = pygame.image.load(source_path("image/background.png"))
bird_wing_up = bird_wing_up_copy = pygame.image.load(source_path("image/bird_wing_up.png"))
bird_wing_down = bird_wing_down_copy = pygame.image.load(source_path("image/bird_wing_down.png"))
pipe_body = pygame.image.load(source_path("image/pipe_body.png"))
pipe_end = pygame.image.load(source_path("image/pipe_end.png"))
score_images = []
for i in range(10):
    number = pygame.image.load(source_path(f"image/{i}.svg"))
    number = pygame.transform.scale(number, (50, 85))
    score_images.append(number)


class Button():
    def __init__(self, screen, msg, center):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = font
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



# 画出管道
def draw_pipes():
    global pipes
    for n in range(len(pipes)):
        for m in range(pipes[n][1]):
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        for m in range(pipes[n][1] + 6, 16):
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1]) * 32))
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1] + 5) * 32))
        pipes[n][0] -= 1


# 设置小鸟
def draw_bird(x, y):
    global frame
    if 0 <= frame <= 82:
        gameScreen.blit(bird_wing_up, (x, y))
        frame += 1
    elif 83 <= frame <= 165:
        gameScreen.blit(bird_wing_down, (x, y))
        frame += 1
        if frame == 165:
            frame = 0


# 检测小鸟状态
def safe():
    if bird[1] > map_height-35:
        print("hit floor")
        return False
    if bird[1] < 0:
        print("hit ceiling")
        return False
    if pipes[0][0]-30 < bird[0] < pipes[0][0] + 79:
        if bird[1] < (pipes[0][1]+1) * 32 or bird[1] > (pipes[0][1]+4) * 32:
            print("hit pipe")
            return False
    return True


# 重置游戏
def reset():
    global frame, map_height, map_width, FPS, pipes, bird, gravity, velocity, score, font
    map_width = 400
    map_height = 512
    frame = 0
    FPS = 165
    pipes.clear()
    bird.clear()
    pipes = [[200, 4]]
    bird = [20, 256]
    gravity = 0.03
    velocity = 0
    score = 0


# 画出得分
"""
def draw_score():
    global score
    s = str(score)
    for i in range(len(s)):
        gameScreen.blit(score_images[int(s[i])], )
"""


def gameloop():
    # 引用变量
    global velocity, bird_wing_up, bird_wing_down, score
    while True:
        # 增加与删除管道
        if len(pipes) < 3:
            x = pipes[-1][0] + 250  # 在右方相距200的位置添加新管道
            open_pos = randrange(1, 9)  # 确定开口位置
            pipes.append([x, open_pos])
        if pipes[0][0] < -100:
            pipes.pop(0)
        # 画出画布
        gameScreen.blit(background, (0, 0))
        gameScreen.blit(background, (284, 0))
        draw_bird(bird[0], bird[1])
        # 监测键盘活动使小鸟跳跃或退出游戏
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird[1] -= 40
                velocity = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        # 设置下坠速度
        velocity += gravity
        bird[1] += velocity
        # 小鸟旋转
        bird_wing_down = pygame.transform.rotate(bird_wing_down_copy, -90 * (velocity / 5))
        bird_wing_up = pygame.transform.rotate(bird_wing_up_copy, -90 * (velocity / 5))
        # 画出管道
        draw_pipes()
        # 记录得分
        if bird[0] == pipes[0][0]:
            score += 1
        s = str(score)
        text_s = f"当前得分:{s}"
        textSurface = font.render(text_s, True, (0, 0, 0))
        gameScreen.blit(textSurface, (20, 10))
        pygame.display.update()
        # 储存
        pygame.display.set_caption("flappybird")
        pygame.display.update()
        # 检测游戏重置
        if not safe():
            record = 0
            if os.path.exists(source_path("record.txt")):
                with open(source_path("record.txt"), "r") as f:
                    record = f.read()
            if score > int(record):
                record = score
                with open(source_path("record.txt"), "w") as f:
                    f.write(str(score))
            text = f"最高分: {record}"
            textSurface = font.render(text, True, (0, 0, 0))
            gameScreen.blit(textSurface, (115, 450))
            play_button = Button(gameScreen, "继续", (200, 200))
            play_button.draw_button()
            esc_button = Button(gameScreen, "退出", (200, 290))
            esc_button.draw_button()
            pygame.display.update()
            flag = True
            while flag:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        flag = False
                        break

                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        return

            reset()
        clock.tick(FPS)


gameloop()
