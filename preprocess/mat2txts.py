"""
File for data preprocessing
Load the label data from the original .mat files and store them into txt files
Converting the labels format between "corner" and "midpoint"
"""
import numpy as np
import h5py
def get_name(index, hdf5_data):

    name_ref = hdf5_data['digitStruct']['name'][index].item()
    name = ''.join([chr(v[0]) for v in hdf5_data[name_ref]])

    return name


def get_bbox(index, hdf5_data):

    attrs = {}
    bbox_ref = hdf5_data['digitStruct']['bbox'][index].item()
    for key in ['label', 'left', 'top', 'width', 'height']:
        attr = hdf5_data[bbox_ref][key]
        values = [hdf5_data[attr[i].item()][0][0].astype(int) \
                  for i in range(len(attr))] if len(attr) > 1 else [attr[0][0]]
        attrs[key] = values

    return attrs


def ltwh_to_ltrb(bbox_ltwh):

    bbox_ltrb = {}
    bbox_ltrb['label'] = (np.array(bbox_ltwh['label']) % 10).tolist()
    bbox_ltrb['left'] = bbox_ltwh['left']
    bbox_ltrb['top'] = bbox_ltwh['top']
    bbox_ltrb['right'] = np.add(bbox_ltwh['left'], bbox_ltwh['width']).tolist()
    bbox_ltrb['bottom'] = np.add(bbox_ltwh['top'], bbox_ltwh['height']).tolist()

    return bbox_ltrb

def ltwh_to_xywh(bbox_ltwh):

    bbox_xywh = {}
    bbox_xywh['label'] = (np.array(bbox_ltwh['label']) % 10).tolist()
    bbox_xywh['mid_x'] = np.add(bbox_ltwh['left'], 0.5 * np.array(bbox_ltwh['width'])).tolist()
    bbox_xywh['mid_y'] = np.add(bbox_ltwh['top'], 0.5 * np.array(bbox_ltwh['height'])).tolist()
    bbox_xywh['width'] = bbox_ltwh['width']
    bbox_xywh['height'] = bbox_ltwh['height']

    return bbox_xywh


def mat_to_txt(txtfile, hdf5_data, format):
    with open(txtfile, 'w') as file:
        for i in range(len(hdf5_data['digitStruct']['name'])):
            bbox = get_bbox(i, hdf5_data)

            if format == 'original':
                bbox_str = ''
                bbox_str += get_name(i, hdf5_data)
                bbox_str += ' '
                for j in range(len(bbox['label'])):
                    bbox_str += ''.join(str(bbox['label'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['left'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['top'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['width'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['height'][j]))
                    bbox_str += ' '

            if format == 'corner':
                bbox = ltwh_to_ltrb(bbox)
                bbox_str = ''
                bbox_str += get_name(i, hdf5_data)
                bbox_str += ' '
                for j in range(len(bbox['label'])):
                    bbox_str += ''.join(str(bbox['label'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['left'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['top'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['right'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['bottom'][j]))
                    bbox_str += ' '

            if format == 'midpoint':
                bbox = ltwh_to_xywh(bbox)
                bbox_str = ''
                bbox_str += get_name(i, hdf5_data)
                bbox_str += ' '
                for j in range(len(bbox['label'])):
                    bbox_str += ''.join(str(bbox['label'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['mid_x'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['mid_y'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['width'][j]))
                    bbox_str += ','
                    bbox_str += ''.join(str(bbox['height'][j]))
                    bbox_str += ' '

            file.write(bbox_str[:-1])
            file.write('\n')
    return


def txt_to_txts(txt_path, dir_path):

    ori_file = open(txt_path, "r").readlines()

    for line in ori_file:
        name = line.split(".")[0]
        txt_name = dir_path + name + ".txt"
        with open(txt_name, mode="w", newline="") as new_file:
            label = line.split(" ")[1:]
            for i in range(len(label)):
                new_file.write(label[i])
                new_file.write('\n')

    return





if __name__ == "__main__":

    # train_path = '/home/yangfei/PycharmProjects/ssd-pytorch-master/SVHN/train/VOC2007/JEPGImages/digitStruct.mat'
    # hdf5_data_train = h5py.File(train_path, 'r')

    test_path = '/SVHN/test/VOC2007/JEPGImages/digitStruct.mat'
    hdf5_data_test = h5py.File(test_path, 'r')

    # print("(train) Converting .mat file to .txt file ...")
    # mat_to_txt('/home/yangfei/PycharmProjects/ssd-pytorch-master/SVHN/train/VOC2007/train.txt', hdf5_data_train, 'midpoint')
    #
    # print("(train) Generating .txt files for each image ...")
    # txt_to_txts('/home/yangfei/PycharmProjects/ssd-pytorch-master/SVHN/train/train.txt',
    #             "/home/yangfei/PycharmProjects/ssd-pytorch-master/SVHN/train/VOC2007/labels/")

    print("(test) Converting .mat file to .txt file ...")
    mat_to_txt('/home/yangfei/PycharmProjects/ssd-pytorch-master/SVHN/test/VOC2007/test.txt', hdf5_data_test, 'midpoint')

    print("(test) Generating .txt files for each image ...")
    txt_to_txts('/SVHN/test/VOC2007/test.txt',
                "/SVHN/test/VOC2007/labels/")