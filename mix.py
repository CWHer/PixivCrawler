# from:https://github.com/NoisyWinds/puzzle/blob/master/puzzle.py
# 大致流程
#   if FIRST_TIME 图片库->色块
#   遍历图片,选取距离最小的色块
#
# 我觉得这个算法不能得出总距离最小
# (以下都是口胡的,下次就写)
# 一些改进的想法:
#   1. 按照以距离为权值的优先队列填补输出图片
#       本质上还是一个贪心,但是我觉得效果应该比目前的好
#   2. 最小费用最大流
#       按照以下方式建图:
#           S --(cap:REPEAT_TIMES,cost:0)--> lib(n)
#           lib(n) --(cap:1,cost:dist)-->target_block(m)
#           target_block(m) --(cap:1,cost:0)--> T
#       但是这样图建出来很大,总共有n+n*m+m条边
#       一个近似优化:
#           每个lib和最近的K个target_block连边
#           每个target_block和最近的K个lib连边
#          图片比较多的情况,我猜K=5应该差不多
#       复杂度O(nm)建图+MCMF,再优化可以考虑套个KD Tree
#   其它的我也想不到了orz
import os
from PIL import Image, ImageOps
import argparse
import time
import random
import math
import sys
from colorsys import rgb_to_hsv
import re


def get_avg_color(img):
    width, height = img.size
    pixels = img.load()
    if type(pixels) is int:
        raise IOError("PIL load image failed")
    data = []
    for x in range(width):
        for y in range(height):
            data.append(pixels[x, y])
    h = s = v = count = 0
    for i in range(len(data)):
        r = data[i][0]
        g = data[i][1]
        b = data[i][2]
        count += 1
        hsv = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        h += hsv[0]
        s += hsv[1]
        v += hsv[2]
    hAvg = round(h / count, 3)
    sAvg = round(s / count, 3)
    vAvg = round(v / count, 3)
    if count == 0:
        raise IOError("load image failed")
    return (hAvg, sAvg, vAvg)


def find_closiest(color, colors_list):
    cur_closer = False
    arr_len = 0
    dist = DIFF_DIST
    for img in colors_list:
        n_diff = math.sqrt(
            math.pow(math.fabs(color[0] - img[0]), 2) +
            math.pow(math.fabs(color[1] - img[1]), 2) +
            math.pow(math.fabs(color[2] - img[2]), 2))
        if n_diff < dist and img[3] <= REPEAT_TIMES:
            dist = n_diff
            cur_closer = img
    if not cur_closer:
        raise ValueError(
            "no enough approximate picture. recommend increase REPEAT_TIMES")
    cur_closer[3] += 1
    return "({}, {}, {})".format(cur_closer[0], cur_closer[1], cur_closer[2])


def make_puzzle(img, color_list):
    width, height = img.size
    print("Width = {}, Height = {}".format(width, height))
    background = Image.new('RGB', img.size, (255, 255, 255))
    total_images = math.floor((width * height) / (SLICE_SIZE * SLICE_SIZE))
    images_cnt = 0
    for y in range(0, height, SLICE_SIZE):
        for x in range(0, width, SLICE_SIZE):
            images_cnt += 1
            try:
                block = img.crop((x, y, x + SLICE_SIZE, y + SLICE_SIZE))
                block = get_avg_color(block)
                close_img_name = find_closiest(block, color_list)
                close_img_name = OUT_DIR + str(close_img_name) + '.jpg'
                paste_img = Image.open(close_img_name)
                bar_size = math.floor(images_cnt / total_images * 100)
                log = "\r[{}{}]{}%".format("#" * bar_size,
                                           " " * (100 - bar_size), bar_size)
                print(log, end='')
                background.paste(paste_img, (x, y))
            except Exception as e:
                print(e)
                print('\ncreate ' + str(x) + ',' + str(y) + ' failed')
    return background


def get_image_paths():
    paths = []
    suffixes = ['jpg']
    for item in os.listdir(IN_DIR):
        suffix = item[item.rfind('.') + 1:len(item)]
        if suffix not in suffixes:
            print("not jpg image:%s" % item)
            continue
        paths.append(IN_DIR + item)
    if len(paths) == 0:
        raise IOError("none image is found")
    print("images found: " + str(len(paths)))
    return paths


def resize_pic(in_name, width, height=None):
    if height == None: height = width
    img = Image.open(in_name)
    img = ImageOps.fit(img, (width, height), Image.ANTIALIAS)
    return img


def convert_image(path):
    try:
        img = resize_pic(path, SLICE_SIZE)
        color = get_avg_color(img)
        img.save(str(OUT_DIR) + str(color) + ".jpg")
    except:
        return False


def convert_all_images():
    paths = get_image_paths()
    num = 0
    print("creating image blocks...")
    for item in paths:
        num += 1
        convert_image(item)
        print('\rnum: ' + str(num), end='')
    print("\nconvert complete")


def read_img_db():
    img_db = []
    for item in os.listdir(OUT_DIR):
        if item != 'None.jpg':
            item = item.split('.jpg')[0]
            item = list(map(float, item[1:-1].split(',')))
            item.append(0)
            img_db.append(item)
    return img_db


SLICE_SIZE = 100
WIDTH = 7500
HEIGHT = 5000
IN_DIR = "images/"
OUT_DIR = "images_lib/"
DIFF_DIST = 1000
REPEAT_TIMES = 1

start_time = time.time()
FIRST_TIME = False
if FIRST_TIME: convert_all_images()
image = 'images/82878621_p1.jpg'
img = resize_pic(image, WIDTH, HEIGHT)
list_of_imgs = read_img_db()
result = make_puzzle(img, list_of_imgs)
# blend target&result
img = Image.blend(result, img, 0.5)
img.save('out.jpg')
print('\nDone')
print("time consumed: %.3f" % (time.time() - start_time))