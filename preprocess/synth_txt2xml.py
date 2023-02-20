#! /usr/bin/python
# -*- coding:UTF-8 -*-
import os, sys
import glob
from PIL import Image

# 图像存储位置
src_img_dir = "/home/yangfei/Datasets/SynthText-digits-only/VOCdevkit/VOC2007/JPEGImages/"
# 图像的 ground truth 的 txt 文件存放位置
src_txt_dir = "/home/yangfei/Datasets/SynthText-digits-only/VOCdevkit/VOC2007/labels/"
src_xml_dir = "/home/yangfei/Datasets/SynthText-digits-only/VOCdevkit/VOC2007/Annotations/"

img_Lists = glob.glob(src_img_dir + '/*.jpg')

img_basenames = []  # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = []  # e.g. 100
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

for img in img_names:
    im = Image.open((src_img_dir + '/' + img + '.jpg'))
    width, height = im.size
    print(img)
    # open the crospronding txt file
    gt = open(src_txt_dir + '/' + img + '.txt').read().splitlines()
    print(gt)

    print(gt[0][0:3])
    if gt[0][0:3] != '0.0':

        # gt = open(src_txt_dir + '/gt_' + img + '.txt').read().splitlines()

        # write in xml file
        # os.mknod(src_xml_dir + '/' + img + '.xml')
        xml_file = open((src_xml_dir + '/' + img + '.xml'), 'w')
        xml_file.write('<annotation>\n')
        xml_file.write('    <folder>VOC2007</folder>\n')
        xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')

        # write the region of image on xml file
        for img_each_label in gt:

            spt = img_each_label.split(',')  # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
            if len(spt) == 5:
                bbox_width = int(spt[3]) - int(spt[1])
                bbox_height = int(spt[4]) - int(spt[2])
                if bbox_width != 0 and bbox_height != 0:
                    bbox_aspect = float(bbox_width / bbox_height)
                elif bbox_width == 0:
                    bbox_aspect = 0
                else:
                    bbox_aspect = 100
                xml_file.write('    <object>\n')
                xml_file.write('        <name>' + str(spt[0]) + '</name>\n')
                xml_file.write('        <pose>Unspecified</pose>\n')
                xml_file.write('        <truncated>0</truncated>\n')
                xml_file.write('        <difficult>0</difficult>\n')
                xml_file.write('        <bndbox>\n')
                xml_file.write('            <xmin>' + str(spt[1]) + '</xmin>\n')
                xml_file.write('            <ymin>' + str(int(spt[2])) + '</ymin>\n')
                xml_file.write('            <xmax>' + str(spt[3]) + '</xmax>\n')
                xml_file.write('            <ymax>' + str(int(spt[4])) + '</ymax>\n')
                # if 0.3 < bbox_aspect < 3:
                #     xml_file.write('            <xmin>' + str(spt[1]) + '</xmin>\n')
                #     xml_file.write('            <ymin>' + str(int(spt[2])) + '</ymin>\n')
                #     xml_file.write('            <xmax>' + str(spt[3]) + '</xmax>\n')
                #     xml_file.write('            <ymax>' + str(int(spt[4])) + '</ymax>\n')
                # elif bbox_aspect < 0.3:
                #     xml_file.write('            <xmin>' + str(int(spt[1]) - int(bbox_height / 3)) + '</xmin>\n')
                #     xml_file.write('            <ymin>' + str(int(spt[2])) + '</ymin>\n')
                #     xml_file.write('            <xmax>' + str(int(spt[3]) + int(bbox_height / 3)) + '</xmax>\n')
                #     xml_file.write('            <ymax>' + str(int(spt[4])) + '</ymax>\n')
                # else:
                #     xml_file.write('            <xmin>' + str(spt[1]) + '</xmin>\n')
                #     xml_file.write('            <ymin>' + str(int(spt[2]) - int(bbox_width * 3)) + '</ymin>\n')
                #     xml_file.write('            <xmax>' + str(spt[3]) + '</xmax>\n')
                #     xml_file.write('            <ymax>' + str(int(spt[4]) + int(bbox_width * 3)) + '</ymax>\n')
                xml_file.write('        </bndbox>\n')
                xml_file.write('    </object>\n')
            else:
                break
        xml_file.write('</annotation>')
    else:
        continue
