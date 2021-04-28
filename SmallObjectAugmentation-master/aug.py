# import glob
import cv2 as cv2
import numpy as np
# from PIL import Image
import random
import math
from os.path import basename, split, join, dirname
from util import *


def find_str(filename):
    if 'train' in filename:
        return dirname(filename[filename.find('train'):])
    else:
        return dirname(filename[filename.find('val'):])


def convert_all_boxes(shape, anno_infos, yolo_label_txt_dir):
    height, width, n = shape
    label_file = open(yolo_label_txt_dir, 'w')
    for anno_info in anno_infos:
        target_id, x1, y1, x2, y2 = anno_info
        b = (float(x1), float(x2), float(y1), float(y2))
        bb = convert((width, height), b)
        label_file.write(
            str(target_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def save_crop_image(save_crop_base_dir, image_dir, idx, roi):
    crop_save_dir = join(save_crop_base_dir, find_str(image_dir))
    check_dir(crop_save_dir)
    crop_img_save_dir = join(
        crop_save_dir,
        basename(image_dir)[:-3] + '_crop_' + str(idx) + '.jpg')
    cv2.imwrite(crop_img_save_dir, roi)


def GaussianBlurImg(image):
    # 高斯模糊
    ran = random.randint(0, 9)
    if ran % 2 == 1:
        image = cv2.GaussianBlur(image, ksize=(ran, ran), sigmaX=0, sigmaY=0)
    else:
        pass
    return image


def roi_resize(image, small_pic_width,small_pic_height):
    # 改变小图片大小
    height, width, channels = image.shape

    image = cv2.resize(image, (small_pic_width,small_pic_height), interpolation=cv2.INTER_AREA)   # 注意，目标size不能太大，否则图片会不够大小贴下目标

    return image


def get_resolution(image):
    '''
    获得背景图的分辨率以调整 粘贴小图像的大小，防止因小图像太大导致粘贴不上去
    :param image:
    :return:
    '''

    image = cv2.imread(image)
    height, width, channels = image.shape
    print('height', height, 'width', width)

    # 根据你的背景图的大小进行调整
    if width>=2500 and height>=2500:
        small_pic_width = 120
        small_pic_height = 120

    elif (width>=1920 and width<2500) and (height>=1080 and height<2500):
        small_pic_width = 60
        small_pic_height = 60

    elif width<=1300 and height<=1300:
        small_pic_width = 30
        small_pic_height = 30

    else:
        small_pic_width = 40
        small_pic_height = 40

    return height,width,small_pic_width,small_pic_height



def copysmallobjects(image_dir, label_dir, save_tianya_pic, save_tianya_txt, small_img_dir,
                      times, cl_id):
    image = cv2.imread(image_dir)
    print('image_dir2',image_dir)

    labels = read_label_txt(label_dir)
    if len(labels) == 0:
        return

    height,width,small_pic_width, small_pic_height = get_resolution(image_dir)
    # 分辨率太低的图片会被过滤掉
    if height<=500 and width<=500:
        return

    # yolo txt转化为x1y1x2y2
    rescale_labels = rescale_yolo_labels(labels, image.shape)  # 转换坐标表示
    # print("org bbox:", rescale_labels)  # 原图像bbox集合
    all_boxes = []

    for _, rescale_label in enumerate(rescale_labels):
        all_boxes.append(rescale_label)

    for small_img_dirs in small_img_dir:
        image_bbox = cv2.imread(small_img_dirs)
        print('+++{} image_bbox'.format(image_dir))
        # from 3000 to 1500


        roi = roi_resize(image_bbox, small_pic_width,small_pic_height)  # 对roi图像做缩放
        print('==={}'.format(image_dir), rescale_labels)
        new_bboxes = random_add_patches(roi.shape,     # 此函数roi目标贴到原图像上，返回的bbox为roi在原图上的bbox,
                                         rescale_labels,  # 并且bbox不会挡住图片上原有的目标
                                         image.shape,
                                         paste_number=2,  # 将该roi目标复制几次并贴到到原图上
                                         iou_thresh=0,
                                         cl_id=cl_id)    # iou_thresh 原图上的bbox和贴上去的roi的bbox的阈值
        print('{} new_bbox'.format(image_dir),new_bboxes)
        count = 0
        # print("end patch")
        for new_bbox in new_bboxes:
            count += 1

            cl, bbox_left, bbox_top, bbox_right, bbox_bottom = new_bbox[0], new_bbox[1], new_bbox[2], new_bbox[3], \
                                                               new_bbox[4]
            # roi = GaussianBlurImg(roi)  # 高斯模糊
            height, width, channels = roi.shape
            center = (int(width / 2), int(height / 2))
            #ran_point = (int((bbox_top+bbox_bottom)/2),int((bbox_left+bbox_right)/2))
            mask = 255 * np.ones(roi.shape, roi.dtype)
            # print("before try")
            try:
                if count > 1:  # 如果count>1,说明paste_number大于1次，对roi做一个翻转变换
                    roi = flip_bbox(roi)
                image[bbox_top:bbox_bottom, bbox_left:
                      bbox_right] = cv2.seamlessClone(
                          roi,
                          image[bbox_top:bbox_bottom, bbox_left:bbox_right],
                          mask, center, cv2.NORMAL_CLONE)
                all_boxes.append(new_bbox)
                rescale_labels.append(new_bbox)

                # print("end try")
            except ValueError:
                # print("---")
                continue

    print('before {} is ok'.format(image_dir))
    dir_name = find_str(image_dir)
    save_txt = join(save_tianya_txt, dir_name)
    save_pic = join(save_tianya_pic, dir_name)
    check_dir(save_txt)
    check_dir(save_pic)
    yolo_txt_dir = join(save_txt, basename(image_dir.replace('.jpg', '_aug_%s.txt' % str(times))))
    cv2.imwrite(join(save_pic, basename(image_dir).replace('.jpg', '_aug_%s.jpg' % str(times))), image)
    convert_all_boxes(image.shape, all_boxes, yolo_txt_dir)

    print('after {} is ok'.format(image_dir))