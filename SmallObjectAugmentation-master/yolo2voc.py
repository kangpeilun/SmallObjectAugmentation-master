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


def makexml(picPath,txtPath,xmlPath='./Annotations'):  # txt所在文件夹路径，xml文件保存路径，图片所在文件夹路径
    """此函数用于将yolo格式txt标注文件转换为voc格式xml标注文件

    在自己的标注图片文件夹下建三 个子文件夹，分别命名为picture、txt、xml
    """

    # 创建字典用来对类型进行转换
    # 此处的字典要与自己的classes.txt文件中的类对应，且顺序要一致
    dic = {0:"caolvjie", 1:"hebianlvcie", 2:"huangcie", 3:"liulanyejia", 4:"mapichun", 5:"meiguobaie",
           6:"renwenwudenge", 7:"ribenjijiding", 8:"sangtianniu", 9:"shuangtiane", 10:"sidaifengdie",
           11:"songmotianniu", 12:"xingtianniu", 13:"yangshanzhoue", 14:"yangxiaozhoue"}

    check_dir(xmlPath)

    files = os.listdir(txtPath)
    for i, name in tqdm(enumerate(files)):
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(os.path.join(txtPath, name))
        txtList = txtFile.readlines()
        # print('txtList',txtList)
        img = cv2.imread(os.path.join(picPath, name[0:-4]+".jpg"))
        # print(os.path.join(picPath, name[0:-4]+".jpg"))
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        foldercontent = xmlBuilder.createTextNode("driving_annotation_dataset")
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenamecontent = xmlBuilder.createTextNode(name[0:-4] + ".jpg")
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # filename标签结束

        size = xmlBuilder.createElement("size")  # size标签
        width = xmlBuilder.createElement("width")  # size子标签width
        widthcontent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthcontent)
        size.appendChild(width)  # size子标签width结束

        height = xmlBuilder.createElement("height")  # size子标签height
        heightcontent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightcontent)
        size.appendChild(height)  # size子标签height结束

        depth = xmlBuilder.createElement("depth")  # size子标签depth
        depthcontent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthcontent)
        size.appendChild(depth)  # size子标签depth结束

        annotation.appendChild(size)  # size标签结束

        for j in txtList:
            oneline = j.strip().split(" ")
            # print('oneline[0]',oneline[0], type(oneline[0]))
            object = xmlBuilder.createElement("object")  # object 标签
            picname = xmlBuilder.createElement("name")  # name标签
            namecontent = xmlBuilder.createTextNode(dic[int(oneline[0])])
            picname.appendChild(namecontent)
            object.appendChild(picname)  # name标签结束

            pose = xmlBuilder.createElement("pose")  # pose标签
            posecontent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束

            truncated = xmlBuilder.createElement("truncated")  # truncated标签
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)  # truncated标签结束

            difficult = xmlBuilder.createElement("difficult")  # difficult标签
            difficultcontent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultcontent)
            object.appendChild(difficult)  # difficult标签结束

            bndbox = xmlBuilder.createElement("bndbox")  # bndbox标签
            xmin = xmlBuilder.createElement("xmin")  # xmin标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)  # xmin标签结束

            ymin = xmlBuilder.createElement("ymin")  # ymin标签
            mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)  # ymin标签结束

            xmax = xmlBuilder.createElement("xmax")  # xmax标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)  # xmax标签结束

            ymax = xmlBuilder.createElement("ymax")  # ymax标签
            mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)  # ymax标签结束

            object.appendChild(bndbox)  # bndbox标签结束

            annotation.appendChild(object)  # object标签结束

        f = open(os.path.join(xmlPath, name[0:-4]+'.xml'), 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()


if __name__ == '__main__':
    picPath='./save_pic'
    txtPath='./save_txt'
    makexml(picPath, txtPath)