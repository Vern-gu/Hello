from PIL import Image
import argparse


parser = argparse.ArgumentParser(description="transfer image to ASCII")
parser.add_argument('file', help='image path')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)
args = parser.parse_args()
img = args.file
width = args.width
height = args.height


def get_ascii_char(r,g,b,alpha=256):
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    if alpha == 0:
        return ' '
    gray = int((19595 * r + 38469 * g + 7474 * b) >> 16)
    # gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = 256.0/len(ascii_char)
    return ascii_char[int(gray/unit)]


def process_image():
    txt = ''
    im = Image.open(img)
    im = im.resize((width,height),Image.NEAREST)
    for h in range(height):
        for w in range(width):
            txt += get_ascii_char(*im.getpixel((w,h)))
        txt += '\n'
    print(txt)
    with open(str(img)[2:6]+'.txt','w') as f:
        f.write(txt)
    # return txt


if __name__ == '__main__':
    process_image()
