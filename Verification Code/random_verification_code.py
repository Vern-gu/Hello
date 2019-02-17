from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


def random_color():
    r = random.randint(64, 255)
    g = random.randint(64, 255)
    b = random.randint(64, 255)
    return r, g, b


def random_color2():
    r = random.randint(32, 127)
    g = random.randint(32, 127)
    b = random.randint(32, 127)
    return r, g, b


def random_char():
    return chr(random.randint(65, 90))  # 随机字母


def random_font():
    base_dir = 'C:\Windows\Fonts\\'
    fonts = ['impact.ttf', 'Inkfree.ttf', 'LATINWD.TTF', 'HoboStd.otf', 'OCRAStd.otf']
    # print(base_dir+random.choice(fonts))
    return base_dir + random.choice(fonts)  # 随机字体


def image():
    width = 240
    height = 60
    im = Image.new('RGB', (width, height), (255, 255, 255))  # 创建画布对象
    font = ImageFont.truetype(random_font(), 36)  # 创建字体对象
    draw = ImageDraw.Draw(im)  # 创建画笔对象
    for h in range(height):
        for w in range(width):
            draw.point((w, h), fill=random_color())  # draw.point画点
    for i in range(4):
        draw.text((60 * i + 15, 10), random_char(), random_color(), font)  # 画文本
    im = im.filter(ImageFilter.BLUR)  # 最后为图片添加模糊效果
    im.save('code.gif', 'gif')


if __name__ == '__main__':
    image()
