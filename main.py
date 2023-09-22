import math
import random
import pyglet
from pyglet.image import ImageGrid
from pyglet.window import Window, mouse, gl
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.shapes import Circle
from pyglet.text import Label

win_width = 1280
win_height = 720

set_plane = input("请输入敌方飞机数目：")
# 飞机,舰船移动速度
p_speed = float(input("请输入飞机速度：（例如4.5）"))
b_speed = float(input("请输入舰船速度：（例如3）"))

window = pyglet.window.Window(
    win_width, win_height,
    resizable=False,  # Make sure it is not resizable
    caption="空战演示",  # Caption of window
    config=pyglet.gl.Config(double_buffer=True),  # Avoids flickers
    vsync=False)


# 加载背景
background = pyglet.image.load('fig/background2.png', decoder=PNGImageDecoder())
bg = pyglet.sprite.Sprite(background, x=0, y=0)

red1_speed = [random.randint(-5, -1), 0]
red2_speed = [random.randint(-5, -1), 0]
red3_speed = [random.randint(-5, -1), 0]
# boat1_speed = [random.randint(-3, -1), random.randint(-3, -1)]

# 加载蓝色飞机
blue = pyglet.image.load('fig/260_0000_蓝色飞机.png', decoder=PNGImageDecoder())
# 飞机雷达范围为100
plane_radar_radius = 100
# blue1从东北海域出发
blue1 = pyglet.sprite.Sprite(blue, x=1200, y=700)
blue1.scale = 0.1
blue1_radar = Circle(blue1.x, blue1.y, plane_radar_radius, color=(0, 0, 100, 100))

blue2 = pyglet.sprite.Sprite(blue, x=1200, y=10)
blue2.scale = 0.1
blue2_radar = Circle(blue2.x, blue2.y, plane_radar_radius, color=(0, 0, 100, 100))

blue3 = pyglet.sprite.Sprite(blue, x=1250, y=5)
blue3.scale = 0.1
blue3_radar = Circle(blue3.x, blue3.y, plane_radar_radius, color=(0, 0, 100, 100))

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
# 舰艇从厦门港口(307,370)出发
# boat1 = pyglet.sprite.Sprite(boat, x=307, y=370)
# 舰艇从厦门港口(390,410)出发
boat1 = pyglet.sprite.Sprite(boat, x=390, y=410)
boat1.scale = 0.1
# Create a black circle around boat1
# 舰艇雷达范围为150
boat1_radar_radius = 150
boat1_radar = Circle(boat1.x, boat1.y, boat1_radar_radius, color=(100, 0, 0, 100))

x, y = 0, 0

text_spot = Label('Enemy Spotted!',
                  font_name='Arial',
                  font_size=36,
                  color=(0, 0, 0, 255),
                  x=window.width // 2, y=window.height // 2,
                  anchor_x='center', anchor_y='center')

text_fin = Label('Mission Complete!',
                 font_name='Arial',
                 font_size=36,
                 color=(0, 0, 0, 255),
                 x=window.width // 2, y=window.height // 2,
                 anchor_x='center', anchor_y='center')


# 给窗口绑定鼠标事件
@window.event
def on_mouse_motion(_x, _y, dx, dy):
    global x, y
    x, y = _x, _y
    # print("鼠标的坐标", x, y)


@window.event
def on_mouse_press(x, y, button, modifiers):
    # Handle mouse press events here
    pass


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glClearColor(255, 255, 255, 255)
    # 绘制背景
    bg.draw()

    if set_plane == '2':
        # 绘制blue1飞机
        blue1.draw()
        blue1_radar.draw()
        # 绘制blue2飞机
        blue2.draw()
        blue2_radar.draw()
    elif set_plane == '3':
        # 绘制blue1飞机
        blue1.draw()
        blue1_radar.draw()
        # 绘制blue2飞机
        blue2.draw()
        blue2_radar.draw()
        # 绘制blue3飞机
        blue3.draw()
        blue3_radar.draw()
    else:
        # 绘制blue1飞机
        blue1.draw()
        blue1_radar.draw()

    # red1.draw()
    # red2.draw()
    # red3.draw()
    # 加载舰艇
    boat1.draw()
    boat1_radar.draw()
    # 舰艇拦截判定
    attack(blue1, blue1_radar, boat1)
    attack(blue2, blue2_radar, boat1)
    attack(blue3, blue3_radar, boat1)


def finish():
    pyglet.clock.schedule_once(pyglet.app.exit, 3)


def attack(plane, plane_radar, red_boat):
    # 1VN场景下，当所有飞机都被击落时，任务完成
    if not blue1.visible and not blue2.visible and not blue3.visible:
        text_fin.draw()
        finish()
    # 判定飞机距离舰船范围在100以内时，舰艇进行攻击
    if math.sqrt((plane.x - red_boat.x) ** 2 + (plane.y - red_boat.y) ** 2) < 100:
        # print("舰艇攻击:", plane)
        text_spot.draw()
        plane.visible = False
        plane_radar.visible = False
        pyglet.clock.schedule_once(lambda dt: text_spot.delete(), 1)


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
    # 旋转的角度
    # plane.rotation += random.randint(-10,10)
    # print("飞机横坐标：", blue1.x, "飞机纵坐标：", blue1.y)


def plane_move(des_x, des_y, plane, plane_radar):
    dx = des_x - plane.x
    dy = des_y - plane.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    direction_x = dx / distance
    direction_y = dy / distance
    # 将direction_x,direction_y转化成角度，正上方为0度，顺时针增加
    angle = math.degrees(math.atan2(direction_y, direction_x))
    # print(angle)
    # 调整飞机的朝向角度
    plane.rotation = 90 - angle
    # 将飞机的速度设置为移动方向的向量
    plane_speed = [direction_x * p_speed, direction_y * p_speed]
    # 飞机的移动
    move(plane, plane_speed)
    # 飞机雷达的移动
    move(plane_radar, plane_speed)
    # 飞机的边界检测
    # boat1_speed = check_border(boat1, boat1_speed)


def update(dt):
    global x, y, p_speed, b_speed, red1_speed, red2_speed, red3_speed

    # =========舰艇移动===============
    # 计算舰艇需要移动的距离和方向
    # Center the boat1 sprite on its own coordinates
    dx = x - boat1.x
    dy = y - boat1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    direction_x = dx / distance
    direction_y = dy / distance
    # 将direction_x,direction_y转化成角度，正上方为0度，顺时针增加
    angle = math.degrees(math.atan2(direction_y, direction_x))
    # 调整舰艇朝向角度
    boat1.rotation = - angle
    # print(boat1.rotation)
    # 将舰艇的速度设置为移动方向的向量
    boat1_speed = [direction_x * b_speed, direction_y * b_speed]
    move(boat1, boat1_speed)
    move(boat1_radar, boat1_speed)

    # # 飞机的移动
    # blue2.rotation = 90
    # move(blue2, blue2_speed)
    # # 飞机的边界检测
    # blue1_speed = check_border(blue2, blue2_speed)

    # # 飞机的移动
    # blue3.rotation = 90
    # move(blue3, blue3_speed)
    # # 飞机的边界检测
    # blue1_speed = check_border(blue3, blue3_speed)

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

    # =========飞机的移动===============
    # 舰艇以固定速度向台湾岛台北市(685，435)移动
    plane_move(685, 435, blue1, blue1_radar)
    plane_move(685, 435, blue2, blue2_radar)
    plane_move(685, 435, blue3, blue3_radar)

    on_draw()


pyglet.clock.schedule_interval(update, 1 / 6)

pyglet.app.run()
