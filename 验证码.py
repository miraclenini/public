from PIL import Image,ImageFilter,ImageFont,ImageDraw
import random
import string

# 随机字母
# def rndChar():
#
#     return chr(random.randint(65,90)) # 65-90 A-W

# 随机字母和数字
def getandl(num,many):  #num 位数  many 个数
    for x in range(many):
        s = ''
        for i in range(num):
            n = random.randint(1,2)  # n = 1或2 1生成数字 2生产字母
            if n == 1:
                numb = random.randint(0,9)
                s += str(numb)
            else:
                s += str(random.choice(string.ascii_letters)) # string.ascii_letters字母表
    return s

def rndColor():
       return (random.randint(64,255),random.randint(64,255),random.randint(64,255)) #64开始较好显示，字体颜色


def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))  # 64背景颜色

width = 60*4
height = 60

image = Image.new('RGB',(width,height),(255,255,255))
# 指定字体大小
font =ImageFont.truetype('l_10646.ttf',36)  #l_10646.ttf ----字体

# 画笔
draw = ImageDraw.Draw(image)

# 填充每个像素点
for x in range(width):
    for y in range(height):
        draw.point((x,y),fill=rndColor())

for x in range(4):
    draw.text((60*x+10,10),getandl(1,4),font=font,fill=rndColor2()) #起点宽度60*x  高度10，fill颜色填充

image = image.filter(ImageFilter.BLUR)   #  模糊处理
image.show()
