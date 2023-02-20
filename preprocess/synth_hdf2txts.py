import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mpimg  # mpimg 用于读取图片
import numpy as np

from time import sleep
from tqdm import tqdm


f = h5py.File("/home/yangfei/Datasets/SynthText-digits-only/SynthText.h5", "r+")
image_path = '/home/yangfei/Datasets/SynthText-digits-only/VOCdevkit/VOC2007/JPEGImages/'
annotation_path = '/home/yangfei/Datasets/SynthText-digits-only/VOCdevkit/VOC2007/labels/'
cnt = 1

print(f.values)
for key in f.keys():
    # print(key)
    # print(f[key].name)
    # print(f[key].values())
    for value in tqdm(f[key].values()):
        # print(value)
        height = np.array(value).shape[0]
        bbox = value.attrs['charBB']
        chars = value.attrs['txt']
        image_name = value.name.lstrip("/data")

        char_str = chars.flatten()  # 转换为一维数组
        points_bbox = bbox.flatten()    # 转换为一维数组
        # print(points_bbox)
        # print(len(points_bbox))
        txt = []
        for x in range(len(char_str)):
            char_str[x] = char_str[x].replace('\n', '')
            char_str[x] = char_str[x].replace(' ', '')
            if char_str[x] != ' ':
                txt.append(char_str[x])
        txts = "".join(txt)
        txt_name = annotation_path + image_name + ".txt"
        with open(txt_name, mode="w", newline="") as new_file:
            for i in range(len(txts)):
                new_file.write(txts[i])
                new_file.write(',' + str(min(int(points_bbox[i]), int(points_bbox[3 * len(txts) + i]))))    # xmin的坐标
                new_file.write(',' + str(max(int(points_bbox[2 * len(txts) + i + len(txts) * 4]), int(points_bbox[3 * len(txts) + i + len(txts) * 4]))))    # ymin的坐标
                new_file.write(',' + str(max(int(points_bbox[1 * len(txts) + i]), int(points_bbox[2 * len(txts) + i]))))  # xmax的坐标
                new_file.write(',' + str(min(int(points_bbox[i + len(txts) * 4]), int(points_bbox[1 * len(txts) + i + len(txts) * 4]))))  # ymax的坐标
                new_file.write('\n')

        # plt.imshow(np.array(value))  # 显示图片
        # plt.imshow(value)  # 显示图片
        # plt.imsave(image_path + image_name + '.jpg', value)
        plt.axis('off')  # 不显示坐标轴
        # plt.show()
        plt.close()
        cnt = cnt + 1
sleep(0.5)
f.close()

print(str(cnt) + " images and labels have been generated!")

