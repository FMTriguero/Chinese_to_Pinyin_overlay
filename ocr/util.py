import re
import pinyin
import pinyin.cedict
import cv2
import numpy as np


def sort_box(box):
    box = sorted(box, key=lambda x: sum([x[1], x[3], x[5], x[7]]))
    return box


def dump_rotate_image(img, rot_deg, pt1, pt2, pt3, pt4):
    rot_rad = np.radians(rot_deg)
    abs_cos_rot = np.fabs(np.cos(rot_rad))
    abs_sin_rot = np.fabs(np.sin(rot_rad))

    height, width = img.shape[:2]
    height_new = int(width * abs_sin_rot + height * abs_cos_rot)
    width_new = int(height * abs_sin_rot + width * abs_cos_rot)
    rot_mat = cv2.getRotationMatrix2D((width // 2, height // 2), rot_deg, 1)
    rot_mat[0, 2] += (width_new - width) // 2
    rot_mat[1, 2] += (height_new - height) // 2
    image_rotation = cv2.warpAffine(
        img, rot_mat, (width_new, height_new), borderValue=(255, 255, 255))
    pt1 = list(pt1)
    pt3 = list(pt3)

    [[pt1[0]], [pt1[1]]] = np.dot(rot_mat, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(rot_mat, np.array([[pt3[0]], [pt3[1]], [1]]))
    ydim, xdim = image_rotation.shape[:2]

    return image_rotation[
        max(1, int(pt1[1])): min(ydim - 1, int(pt3[1])),
        max(1, int(pt1[0])): min(xdim - 1, int(pt3[0]))
    ]


def contains_chinese(text):
    """Returns whether the given text contains any chinese characters."""
    return re.search(u'[\u4e00-\u9fff]', text)


def get_pinyin(text):
    """Returns the pinyin for the given chinese text."""
    return pinyin.get(text, delimiter=" ")


def get_all_phrase_translations(text):
    """Returns the dictionary translation for all possible
    phrase combinations in the given chinese text."""
    return pinyin.cedict.all_phrase_translations(text)
