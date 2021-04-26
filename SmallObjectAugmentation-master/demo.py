import Helpers as hp
from util import *
import os
from os.path import join
from tqdm import tqdm
import random
import aug as am

base_dir = './'

# 保存你所有的类别，当然可以使用for循环对多个文件进行遍历
class2id = {"caolvjie": 0, "hebianlvcie": 1, "huangcie": 2, "liulanyejia": 3, "mapichun": 4, "meiguobaie": 5,
            "renwenwudenge": 6, "ribenjijiding": 7, "sangtianniu": 8, "shuangtiane": 9, "sidaifengdie": 10,
            "songmotianniu": 11, "xingtianniu": 12, "yangshanzhoue": 13, "yangxiaozhoue": 14}

cl = 'liulanyejia'  # 在这里更改 你要转换的类别
times = 15  # 更改每次在 原图上 添加多少个小图像

cl_id = class2id[cl]
print('cl_id',cl_id)

save_pic = join(base_dir, 'JPEGImages')
save_txt = join(base_dir, 'save_txt')

check_dir(save_pic)
check_dir(save_txt)


# 获取图像的路径，以及图像对应框框的标签
imgs_dir = [os.path.join('.\\background', f) for f in os.listdir('background') if f.endswith('jpg')]
# labels_dir = [os.path.join('.\\txt', f) for f in os.listdir('txt') if f.endswith('txt')]
labels_dir = hp.replace_labels(imgs_dir)  # 原图上目标对应的标签

print(imgs_dir)
print(labels_dir)

small_imgs_dir = [f.strip() for f in open(join(base_dir, 'small.txt')).readlines()]
random.shuffle(small_imgs_dir)
# print('small_imgs_dir',small_imgs_dir)

for image_dir, label_dir in tqdm(zip(imgs_dir, labels_dir)):
    print('image_dir',image_dir)
    small_img = []
    for x in range(times):
        if small_imgs_dir == []:
            #exit()
            small_imgs_dir = [f.strip() for f in open(join(base_dir,'small.txt')).readlines()]
            random.shuffle(small_imgs_dir)

        img_append = small_imgs_dir.pop()
        small_img.append(img_append)

    print('small_img',small_img)

    am.copysmallobjects2(image_dir, label_dir, save_pic, save_txt, small_img, cl_id)
    print('ok')
