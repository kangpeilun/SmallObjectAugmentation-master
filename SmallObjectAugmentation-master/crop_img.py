import shutil
from os.path import join
import glob
import xml.etree.ElementTree as ET
import pickle
from os import listdir, getcwd
import aug
from util import *
from xml.dom.minidom import Document
from tqdm import tqdm
import math


def find_min_size(jpg_list):

    h_min = 2000    # 最短高
    w_min = 2000    # 最短宽
    for jpg in jpg_list:
        img = cv2.imread(jpg)
        h,w,_ = img.shape
        if h < h_min:
            h_min = h
        if w < w_min:
            w_min = w

    return h_min, w_min


def crop_img(data_root, txt_save, save_dir='./crops'):
    '''
    根据bbox截取目标roi，并保存图片，生成截取后的小图片
    :param data_root: 存放原始图片
    :param txt_save: 存放voc2yolo后的txt文件
    :param save_dir: 截取下来的小图片默认存放在 .\small_bbox 文件夹中
    :return:
    '''

    check_dir(save_dir)

    jpg_list = glob.glob(data_root + "/*.jpg")
    txt_list = glob.glob(txt_save + "/*.txt")

    fo = open("small.txt", "w")  # 截图下来的小图片存放的路径

    max_s = -1
    min_s = 1000

    print('jpg_list',jpg_list)
    h_min, w_min = find_min_size(jpg_list)
    print('h_min',h_min,'w_min',w_min)


    for jpg_path,txt_path in zip(jpg_list,txt_list):
        # jpg_path = jpg_list[3]
        # print('jpg_path:',jpg_path)
        jpg_name = os.path.basename(jpg_path)
        # print('jpg_name:',jpg_name)

        # print('txt_path',txt_path)
        f = open(txt_path, "r")

        img = cv2.imread(jpg_path)

        # 防止图片为空的情况，因为这样图片打不开
        if img is not None:
            height, width, channel = img.shape

            # with open('txt_path', 'r') as f:
            #     file_contents = f.readlines()
            file_contents = f.readlines()


            for num, file_content in enumerate(file_contents):
                # print(num, file_content)
                clss, xc, yc, w, h = file_content.split()
                xc, yc, w, h = float(xc), float(yc), float(w), float(h)

                xc *= width
                yc *= height
                w *= width
                h *= height

                max_s = max(w*h, max_s)
                min_s = min(w*h, min_s)

                half_w, half_h = w // 2, h // 2

                x1, y1 = int(xc - half_w), int(yc - half_h)
                x2, y2 = int(xc + half_w), int(yc + half_h)

                crop_img = img[y1:y2, x1:x2]  # 裁剪小图标

                # h, w, _ = crop_img.shape
                # if h > h_min or w > w_min:
                #     crop_img = cv2.resize(crop_img,(math.ceil(h*0.5),math.ceil(w*0.5)))

                new_jpg_name = jpg_name.split('.')[0] + "_crop_" + str(num) + ".jpg"

                print('{} image size'.format(new_jpg_name), crop_img.shape)

                cv2.imwrite(os.path.join(save_dir, new_jpg_name), crop_img)
                # cv2.imshow("croped",crop_img)
                # cv2.waitKey(0)
                fo.write(os.path.join(save_dir, new_jpg_name)+"\n")
        f.close()
    fo.close()
    # print(max_s, min_s)

    # 返回保存截图后小图标的 文件夹路径
    # return save_dir
    

if __name__ == '__main__':
    data_root='./image'
    txt_save='./image_txt'
    crop_img(data_root, txt_save)