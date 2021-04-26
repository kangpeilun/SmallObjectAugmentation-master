import os

imgs_dir = [os.path.join('.\\crops', f) for f in os.listdir('crops') if f.endswith('jpg')]

f = open('./small.txt', 'w')
for path in imgs_dir:
    print(path)

    f.write(path+'\n')

f.close()