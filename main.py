import math
import random
import pyglet
from pyglet.window import Window, mouse, gl
from pyglet.image.codecs.png import PNGImageDecoder

win_width = 1280
win_height = 720

window = pyglet.window.Window(
    win_width, win_height,
    resizable=False,  # Make sure it is not resizable
    caption="空战演示",  # Caption of window
    config=pyglet.gl.Config(double_buffer=True),  # Avoids flickers
    vsync=False)

# 加载背景
background = pyglet.image.load('fig/background2.png', decoder=PNGImageDecoder())
bg = pyglet.sprite.Sprite(background, x=0, y=0)

blue2_speed = [random.randint(1, 5), 0]
blue3_speed = [random.randint(1, 5), 0]
red1_speed = [random.randint(-5, -1), 0]
red2_speed = [random.randint(-5, -1), 0]
red3_speed = [random.randint(-5, -1), 0]
# boat1_speed = [random.randint(-3, -1), random.randint(-3, -1)]

# 加载蓝色飞机
blue = pyglet.image.load('fig/260_0000_蓝色飞机.png', decoder=PNGImageDecoder())
# blue1从厦门港口出发
blue1 = pyglet.sprite.Sprite(blue, x=307, y=370)
blue1.scale = 0.1

blue2 = pyglet.sprite.Sprite(blue, x=260, y=440)
blue2.scale = 0.1

blue3 = pyglet.sprite.Sprite(blue, x=260, y=480)
blue3.scale = 0.1

# 加载红色飞机
red = pyglet.image.load('fig/260_0001_红色飞机.png', decoder=PNGImageDecoder())
red1 = pyglet.sprite.Sprite(red, x=1090, y=400)
red1.scale = 0.1

red2 = pyglet.sprite.Sprite(red, x=1090, y=440)
red2.scale = 0.1

red3 = pyglet.sprite.Sprite(red, x=1090, y=480)
red3.scale = 0.1

# 加载舰艇
boat = pyglet.image.load('fig/舰艇.png', decoder=PNGImageDecoder())
boat1 = pyglet.sprite.Sprite(boat, x=1200, y=600)
boat1.scale = 0.1

# 飞机,舰船移动速度
p_speed = 5
b_speed = 3

x, y = 0, 0


# 给窗口绑定鼠标事件
@window.event
def on_mouse_motion(_x, _y, dx, dy):
    global x, y
    x, y = _x, _y
    # print("鼠标的坐标", x, y)


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glClearColor(255, 255, 255, 255)
    # 绘制背景
    bg.draw()
    # 绘制blue1飞机
    blue1.draw()
    # blue2.draw()
    # blue3.draw()
    # 绘制蓝色飞机
    # red1.draw()
    # red2.draw()
    # red3.draw()
    # 加载舰艇
    boat1.draw()


# 边界检测
def check_border(plane, speed):
    x = plane.x
    y = plane.y
    if x < 0 or x > 1280 - plane.width * plane.scale:
        speed[0] = -speed[0]
    elif y < 0 or y > 720 - plane.height * plane.scale:
        speed[1] = -speed[1]
    return speed


# 飞机移动
def move(plane, speed):
    # 飞机的位置
    plane.x += speed[0]
    plane.y += speed[1]
    # print()
    # 旋转的角度
    # plane.rotation += random.randint(-10,10)
    # print(blue1.x, blue1.y)


def update(dt):
    global x, y, p_speed, b_speed, blue2_speed, blue3_speed, red1_speed, red2_speed, red3_speed, boat1_speed

    # =========blue1移动===============
    # 计算blue1需要移动的距离和方向
    dx = x - blue1.x
    dy = y - blue1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    direction_x = dx / distance
    direction_y = dy / distance
    # 将direction_x,direction_y转化成角度，正上方为0度，顺时针增加
    angle = math.degrees(math.atan2(direction_y, direction_x))
    # 调整blue1朝向角度
    blue1.rotation = 90 - angle
    # 将blue1的速度设置为移动方向的向量
    blue1_speed = [direction_x * p_speed, direction_y * p_speed]
    move(blue1, blue1_speed)

    # 飞机的移动
    blue2.rotation = 90
    move(blue2, blue2_speed)
    # 飞机的边界检测
    blue1_speed = check_border(blue2, blue2_speed)

    # 飞机的移动
    blue3.rotation = 90
    move(blue3, blue3_speed)
    # 飞机的边界检测
    blue1_speed = check_border(blue3, blue3_speed)

    # =========3架红色飞机的移动===============
    red1.rotation = -90
    move(red1, red1_speed)
    # 飞机的边界检测
    red1_speed = check_border(red1, red1_speed)

    # 飞机的移动
    red2.rotation = -90
    move(red2, red2_speed)
    # 飞机的边界检测
    red2_speed = check_border(red2, red2_speed)

    # 飞机的移动
    red3.rotation = -90
    move(red3, red3_speed)
    # 飞机的边界检测
    red3_speed = check_border(red3, red3_speed)

    # =========舰艇的移动===============
    # 舰艇以固定速度向台湾岛台北市(685，435)移动
    dx = 685 - boat1.x
    dy = 435 - boat1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    direction_x = dx / distance
    direction_y = dy / distance
    # 将direction_x,direction_y转化成角度，正上方为0度，顺时针增加
    angle = math.degrees(math.atan2(direction_y, direction_x))
    # print(angle)
    # 调整舰艇的朝向角度
    boat1.rotation = 135 + angle
    # 将舰艇的速度设置为移动方向的向量
    boat1_speed = [direction_x * b_speed, direction_y * b_speed]
    # 舰艇的移动
    move(boat1, boat1_speed)
    # 舰艇的边界检测
    boat1_speed = check_border(boat1, boat1_speed)

    on_draw()


pyglet.clock.schedule_interval(update, 1 / 6)

pyglet.app.run()