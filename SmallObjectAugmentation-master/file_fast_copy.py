import os

'''
    快速生成背景图片
'''

def fast_copy(path):

    files = []
    names = []
    for f in os.listdir(path):
        if not f.endswith("~") or not f == "":  # 返回指定的文件夹包含的文件或文件夹的名字的列表
            files.append(os.path.join(path, f))  # 把目录和文件名合成一个路径
            names.append(f)

    print(files)
    print(names)

    for file_path,name in zip(files,names):
        print('file path:',file_path, 'name:',name)
        # 将文件复制 150 次
        if name.split('.')[1] == 'jpg':
            for num in range(150):
                new_img_name = name.split('.')[0] + str(num+1) + '.jpg'
                print(new_img_name, os.path.join(path,new_img_name))
                os.system('copy {} {}'.format(file_path, os.path.join(path,new_img_name)))


        if name.split('.')[1] == 'txt':
            for num in range(150):
                new_txt_name = name.split('.')[0] + str(num+1) + '.txt'
                print(new_txt_name, os.path.join(path,new_txt_name))
                os.system('copy {} {}'.format(file_path, os.path.join(path,new_txt_name)))


if __name__ == '__main__':
    fast_copy(r'D:\桌面\2021软件杯\code\pestRecognization\SmallObjectAugmentation-master\background')