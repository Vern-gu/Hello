# coding:utf8

import pygame
import random
import os
from pygame.locals import *


pygame.init()
GRID_WIDTH = 20  # 每小格宽度
GRID_NUM_WIDTH = 15  # 宽15小格
GRID_NUM_HEIGHT = 25  # 高25小格
WIDTH, HEIGHT = GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT  
# 游戏屏幕的宽高：300, 500
SIDE_WIDTH = 200  # 侧边框宽度
SCREEN_WIDTH = WIDTH + SIDE_WIDTH  # 屏幕宽度500
WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)

CUBE_COLORS = [   # 方块颜色
    (0xcc, 0x99, 0x99), (0xff, 0xff, 0x99), (0x66, 0x66, 0x99),
    (0x99, 0x00, 0x66), (0xff, 0xcc, 0x00), (0xcc, 0x00, 0x33),
    (0xff, 0x00, 0x33), (0x00, 0x66, 0x99), (0xff, 0xff, 0x33),
    (0x99, 0x00, 0x33), (0xcc, 0xff, 0x66), (0xff, 0x99, 0x00)
]

screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))  # pygame窗口大小设置
pygame.display.set_caption("Tetris")   # pygame窗口标题
clock = pygame.time.Clock()  # pygame内置时钟
FPS = 30

level = 1
score = 0
high_score = 0

screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
# 游戏屏幕内小方格初始化，统一为None（15 × 25）


def init_score():  # 初始化历史最高分，创建本地缓存存储分数
    global high_score
    file = os.path.exists("./score.temp")
    if not file:
        temp = open("score.temp", 'w')
        temp.write("0")
        temp.close()
    temp = open('score.temp', 'r')
    high_score = temp.read()
    temp.close()
    
    
def score_write(sco):  # 写入新成绩
    temp = open('score.temp', 'w')
    temp.write(sco)
    temp.close()
    

def show_text(surf, text, size, x, y, color=WHITE):  # 设置显示文本方法
    font = pygame.font.SysFont('calibri', size)  # pygame文字字体
    text_surface = font.render(text, True, color)  # 设置文字的内容、颜色
    text_rect = text_surface.get_rect()  # 获得文字边框（文本框）
    text_rect.midtop = (x, y)  # 设置文字位置
    surf.blit(text_surface, text_rect)  # 创建文本


class CubeShape(object):
    SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],  # (y,x)(行，列)
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
    L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]
    SHAPES_WITH_DIR = {
        'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z
    }

    def __init__(self):
        self.shape = self.SHAPES[random.randint(0, len(self.SHAPES) - 1)]  # 当前形状
        # 骨牌所在的行列
        self.center = (2, GRID_NUM_WIDTH // 2)  # 骨牌出生点中心坐标
        self.dir = random.randint(0, len(self.SHAPES_WITH_DIR[self.shape]) - 1)  # 当前方向
        self.color = CUBE_COLORS[random.randint(0, len(CUBE_COLORS) - 1)]  # 当前颜色
 
    def get_all_gridpos(self, center=None):  # 获取所有格子的位置
        curr_shape = self.SHAPES_WITH_DIR[self.shape][self.dir]  # 当前形状和方向的骨牌坐标
        if center is None: 
            center = [self.center[0], self.center[1]]  # 初始的骨牌中心坐标

        return [(cube[0] + center[0], cube[1] + center[1])  # 遍历组成骨牌的方块的坐标，
                for cube in curr_shape]                     # 使其所有的坐标都确定，
                                                            # 返回的是一个包含多个坐标的列表
    def conflict(self, center):
        for cube in self.get_all_gridpos(center):  # 遍历当前骨牌所有坐标
            # 超出屏幕之外，说明不合法
            if cube[0] < 0 or cube[1] < 0 or cube[0] >= GRID_NUM_HEIGHT or\
                    cube[1] >= GRID_NUM_WIDTH:
                return True

            # 不为None，说明之前已经有小方块存在了，也不合法
            if screen_color_matrix[cube[0]][cube[1]] is not None:
                return True

        return False

    def rotate(self):
        new_dir = self.dir + 1
        new_dir %= len(self.SHAPES_WITH_DIR[self.shape])  # 使列表的方向循环，不至于越界
        old_dir = self.dir  # 备份一份旧的方向
        self.dir = new_dir
        if self.conflict(self.center):    # 骨牌的定位、移动都是靠的骨牌center坐标
            self.dir = old_dir
            return False

    def down(self):
        center = (self.center[0] + 1, self.center[1])
        if self.conflict(center):  # 冲突返回False
            return False

        self.center = center   # 更新self.center坐标
        return True

    def left(self):
        center = (self.center[0], self.center[1] - 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def right(self):
        center = (self.center[0], self.center[1] + 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def draw(self):  # 画出骨牌
        for cube in self.get_all_gridpos():
            pygame.draw.rect(screen, self.color,
                             (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,  # 坐标，宽，高
                              GRID_WIDTH, GRID_WIDTH))
            # pygame.draw.rect(screen, WHITE,  # 画轮廓线
            #                  (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,
            #                   GRID_WIDTH, GRID_WIDTH),
            #                  1)

            
def draw_grids():  # 画网格线
    for i in range(GRID_NUM_WIDTH):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * GRID_WIDTH, 0), (i * GRID_WIDTH, HEIGHT))

    for i in range(GRID_NUM_HEIGHT):
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * GRID_WIDTH), (WIDTH, i * GRID_WIDTH))

    pygame.draw.line(screen, WHITE,
                     (GRID_WIDTH * GRID_NUM_WIDTH, 0),
                     (GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT))

    
def draw_matrix():  # 画出屏幕内固定的方块
    for i, row in zip(range(GRID_NUM_HEIGHT), screen_color_matrix):
        for j, color in zip(range(GRID_NUM_WIDTH), row):
            if color is not None:
                pygame.draw.rect(screen, color,
                            (j * GRID_WIDTH, i * GRID_WIDTH,
                             GRID_WIDTH, GRID_WIDTH))
                # pygame.draw.rect(screen, WHITE,
                #             (j * GRID_WIDTH, i * GRID_WIDTH,
                #              GRID_WIDTH, GRID_WIDTH), 2)

                
def draw_score():
    show_text(screen, 'SCORE:{}'.format(score), 20, WIDTH + SIDE_WIDTH // 2, 100)
    show_text(screen, 'Best score:%s' % high_score, 20, WIDTH + SIDE_WIDTH // 2, 400)
    
    
def remove_full_line():  # 满行消除
    global screen_color_matrix
    global score
    global level
    new_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
    index = GRID_NUM_HEIGHT - 1
    n_full_line = 0
    for i in range(GRID_NUM_HEIGHT - 1, -1, -1):
        is_full = True
        for j in range(GRID_NUM_WIDTH):  # 遍历游戏屏幕每一个小格
            if screen_color_matrix[i][j] is None:  # 只要第i行有一个格子是None
                is_full = False  # 就判断为这一行没有满
                break  # 跳出子循环
        if not is_full:  # 只要这一行没有满
            new_matrix[index] = screen_color_matrix[i]  # 新的游戏屏幕行就不变
            index -= 1 # 换下一行
        else:
            n_full_line += 1  # 如果满行了，计数加一
    score += n_full_line  # 分数基于消除的行数
    level = score // 20 + 1  # 游戏的难度设置
    screen_color_matrix = new_matrix  # 

    
def show_welcome(screen):
    show_text(screen, 'TETRIS', 30, WIDTH / 2, HEIGHT / 2)
    show_text(screen, 'Press any key to start', 20, WIDTH / 2, HEIGHT / 2 + 50)


init_score（）
running = True
gameover = True
counter = 0
live_cube = None

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if gameover:
                gameover = False
                live_cube = CubeShape()
                break
            if event.key == pygame.K_LEFT:
                live_cube.left()
            elif event.key == pygame.K_RIGHT:
                live_cube.right()
            elif event.key == pygame.K_DOWN:
                live_cube.down()
            elif event.key == pygame.K_UP:
                live_cube.rotate()
            elif event.key == pygame.K_SPACE:
                while live_cube.down() == True:
                    pass
            elif event.key == pygame.K_ESCAPE:  # 定义暂停
                pause = 1
                while pause:
                    for wait in pygame.event.get():
                        if wait.key == pygame.K_SPACE:
                            pause = 0
        remove_full_line()  # 初始化屏幕

    # level 是为了方便游戏的难度，level 越高 FPS // level 的值越小
    # 这样屏幕刷新的就越快，难度就越大
    if gameover is False and counter % (FPS // level) == 0:
        # down 表示下移骨牌，返回False表示下移不成功，可能超过了屏幕或者和之前固定的
        # 小方块冲突了
        if live_cube.down() == False:  # 方块持续下降，直到不能下降为止
            for cube in live_cube.get_all_gridpos():
                screen_color_matrix[cube[0]][cube[1]] = live_cube.color
            live_cube = CubeShape()  # 重新初始化，再生成新的骨牌
            if live_cube.conflict(live_cube.center):  # 如果初始生成的骨牌也冲突，游戏就结束
                gameover = True
                if score > int(high_score):  # 判断是否有新纪录产生
                    high_score = score
                    score_write(str(high_score))
                score = 0
                live_cube = None
                screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
        # 消除满行
        remove_full_line()
    counter += 1
    # 更新屏幕
    screen.fill(BLACK)
    draw_grids()
    draw_matrix()
    draw_score()
    if live_cube is not None:
        live_cube.draw()
    if gameover:
        show_welcome(screen)
    pygame.display.update()
