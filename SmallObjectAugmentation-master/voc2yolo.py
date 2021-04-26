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


def voc2yolo(data_root, xml_root, txt_save='./image_txt'):
    '''
    jpg 和 xml 文件存放还在
    将VOC数据格式转换为yolo格式，注意这个转换和VOCdevkit\VOC2007\voc2yolo4.py 转换的结果文件不同
    :param data_root: 原始图像jpg文件放此文件夹下
    :param xml_root: 存放原始图像的xml文件
    :param txt_save: 新生成txt文件保存在该目录
    :return:
    '''

    check_dir(txt_save)

    # 根据自己的类别去定义
    class2id = {"caolvjie": 0, "hebianlvcie": 1, "huangcie": 2, "liulanyejia": 3, "mapichun": 4, "meiguobaie": 5,
                "renwenwudenge": 6, "ribenjijiding": 7, "sangtianniu": 8, "shuangtiane": 9, "sidaifengdie": 10,
                "songmotianniu": 11, "xingtianniu": 12, "yangshanzhoue": 13, "yangxiaozhoue": 14}

    def convert(size, box):
        dw = 1. / (size[0])
        dh = 1. / (size[1])
        x = (box[0] + box[1]) / 2.0 - 1
        y = (box[2] + box[3]) / 2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)

    def convert_annotation(xmlpath, txt_save, data_path, tmp_file):
        # in_file = open('./test/Annotations/%s.xml'%(image_id),encoding="utf-8")
        # out_file = open(os.path.join(txt_save, tmp_file.replace(".xml", ".txt")), "w")
        tree = ET.parse(xmlpath)
        root = tree.getroot()
        # size = root.find('size')
        # w = int(size.find('width').text)
        # h = int(size.find('height').text)
        image_id = tmp_file.split('.')[0]
        # print(data_path, image_id)
        img = cv2.imread(os.path.join(data_path, image_id) + ".jpg")
        # print('img_path:',os.path.join(data_path, image_id) + ".jpg")
        # print('img:',img)
        if img is not None:
            # os.remove(os.path.join(data_path, image_id) + ".jpg")  # 如果图片为空不存在就将他删掉
            out_file = open(os.path.join(txt_save, tmp_file.replace(".xml", ".txt")), "w")  # 图片不为空时 才生成对应的 txt 标签
            sp = img.shape
            # print(sp)
            # exit()
            h = sp[0]  # height(rows) of image
            w = sp[1]  # width(colums) of image

            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls_ = obj.find('name').text
                if cls_ not in list(class2id.keys()):
                    # print("没有该label: {}".format(cls_))
                    raise OSError
                    # continue
                cls_id = class2id[cls_]
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        else:
            print('{} is None'.format(os.path.join(data_path, image_id) + ".jpg"))


    for tmp_file in os.listdir(xml_root):
        if tmp_file.strip().split('.')[1] != 'xml':
            continue
        # print(tmp_file)
        xmlpath = os.path.join(xml_root, tmp_file)
        convert_annotation(xmlpath, txt_save, data_root, tmp_file)

    # return txt_save


if __name__ == '__main__':
    data_root='./image'  # 分割小图片时使用
    xml_root='./image_xml'
    voc2yolo(data_root, xml_root)