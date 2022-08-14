from turtle import *
from random import randrange
from time import sleep
# 定义变量
bird = [-100, 80]
# 初始化鸟与障碍物的位置
ball = [[240, 0]]
bird_size = 50
ball_size = 80

# 计算鸟到障碍物的距离


def distance(a, b, x, y):
    return ((a-x) ** 2 + (b-y) ** 2) ** 0.5


# 判断鸟是否碰到障碍物
def hit():
    for n in range(len(ball)):
        if distance(ball[n][0], ball[n][1], bird[0], bird[1]) < (bird_size + ball_size) / 2:
            return True
    return False


# 判断鸟是否碰到上界与下界
def inside():
    if bird[1] - bird_size / 2 < -300 or bird[1] + bird_size / 2 > 300:
        return False
    else:
        return True


# 生成鸟与障碍物,鸟的移动以及障碍物的移动
def draw():
    clear()
    """
    生成障碍物并使障碍物向左移动
    """
    for n in range(len(ball)):
        up()
        goto(ball[n][0], ball[n][1])
        dot(ball_size, "green")
        ball[n][0] = ball[n][0] - 3
    """
    生成鸟并使鸟向下移动
    """
    up()
    goto(bird[0], bird[1])
    dot(bird_size, "black")
    bird[1] = bird[1] - 5
    update()


def gameloop():
    global bird, ball, bird_size, ball_size
    """
    在屏幕右方增加小球
    """
    if randrange(40) == 1:
        x = 240
        y = randrange(-300, 300)
        ball.append([x, y])
    """
    删除超出左方屏幕的小球
    """
    if len(ball) != 0:
        if ball[0][0] < -220:
            ball.pop(0)
    draw()
    """
    判断鸟是否满足碰撞的两个条件
    """
    if (not inside()) or hit():
        sleep(3)
        # 重新画鸟
        bird = [-100, 80]
        # 重新画障碍物
        ball = [[240, 0]]
        # 鸟与障碍物的大小
        bird_size = 50
        ball_size = 80
        draw()
    ontimer(gameloop, 30)

# 鸟的运动
def change():
    bird[1] = bird[1] + bird_size


setup(420, 620, 0, 0)
hideturtle()
tracer(False)
bgcolor("light blue")# 背景颜色
# 监听键盘
listen()
onkey(lambda : change(), " ")
gameloop()
done()