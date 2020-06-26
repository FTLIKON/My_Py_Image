import sys, os
from PIL import Image, ImageDraw


val = {} # 二值数组
dx = [-1,-1,-1,0,0,1,1,1] # 八个方向
dy = [-1,0,1,-1,1,1,0,-1]


def two_value(image, G): # G: Integer 图像二值化阀值
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]): # 遍历图片像素点
            g = image.getpixel((x, y))
            if g > G: # 二值化
                val[(x, y)] = 1
            else:
                val[(x, y)] = 0

def clear_noise(image, N): # N: 图片降噪阈值
        val[(0, 0)] = 1
        val[(image.size[0] - 1, image.size[1] - 1)] = 1
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0 # 相同像素点的数量
                L = val[(x, y)] # 当前像素点
                for j in range(8): # 和周围8个像素点进行比较
                    if L == val[(x + dx[j], y + dy[j])]:
                        nearDots += 1
                if nearDots < N: # 小于阈值，删除像素点
                    val[(x, y)] = 0

def save_png(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), val[(x, y)]) # 描绘像素点
    image.save(filename)

for i in range(100):
    path = "image/" + str(i) +  ".png" # 输入路径
    image = Image.open(path)
    image = image.convert('L')
    two_value(image, 230)
    clear_noise(image, 4)
    pathout = "image/" + str(i)+"+"+str(i) + ".png" # 输出路径
    save_png(pathout, image.size)