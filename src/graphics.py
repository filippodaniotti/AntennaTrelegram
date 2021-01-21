from typing import OrderedDict
import cv2
import numpy as np

RESOLUTION_SIZE = (960, 540)
ASPECT_RATIO = float(16/9)

def get_ar(img) -> float:
    # Width / height
    return img.shape[1] / img.shape[0]

def crop(img) -> np.ndarray:
    if get_ar(img) < ASPECT_RATIO:
        new_h = float(img.shape[1] / ASPECT_RATIO)
        cropped_img =  img[1 : int(new_h), :]
    elif get_ar(img) > ASPECT_RATIO:
        new_w = float(img.shape[0] * ASPECT_RATIO)
        dw = float(img.shape[1] - new_w)
        # cropped_img = img[:, int(new_w/2):-int(new_w/2), :]
        cropped_img = img[:, int(dw / 2) : (img.shape[1] - int(dw / 2)), :]
    else:
        cropped_img = img
    return cropped_img

def shrink(img) -> np.ndarray:
    return cv2.resize(img, RESOLUTION_SIZE, interpolation = cv2.INTER_AREA)

def apply_overlay(img, overlay) -> np.ndarray:
    # overlay=shrink(overlay)
    shape = img.shape
    for y in range(shape[0]):
        for x in range(shape[1]):
            if overlay[y][x][3] > 0:
                for color in range(3):
                    img[y][x][color] = overlay[y][x][color]
    return img

def process_image(path_to_img):
    img = cv2.imread(path_to_img, cv2.IMREAD_UNCHANGED) 
    overlay = cv2.imread("./assets/overlay.png", cv2.IMREAD_UNCHANGED)
    if round(get_ar(img), 1) != round(ASPECT_RATIO, 1):
        img = crop(img)
    if img.shape[1 : 2] != RESOLUTION_SIZE:
        img = shrink(img)        
    img = apply_overlay(img, overlay)
    cv2.imwrite('./assets/zaia.jpg', img)