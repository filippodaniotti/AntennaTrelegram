import cv2
import numpy as np

RESOLUTION_SIZE = (960, 540)
ASPECT_RATIO = float(16/9)

DIGIT_OFFSET_W = (333, 362)
DIGIT_OFFSET_H = (456, 500)

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
    shape = img.shape
    for y in range(shape[0]):
        for x in range(shape[1]):
            if overlay[y][x][3] > 0:
                for color in range(3):
                    img[y][x][color] = overlay[y][x][color]
    return img

def set_days(img, days) -> np.ndarray:
    # dw is the width of each single digit
    dw = DIGIT_OFFSET_W[1] - DIGIT_OFFSET_W[0]
    current_digit = cv2.imread(f'./assets/{days[0]}.png', cv2.IMREAD_UNCHANGED)
    # loop through each digit
    for digit in range(len(days)):
        if digit > 0 and days[digit] != days[digit - 1]:
            current_digit = cv2.imread(f'./assets/{days[digit]}.png', cv2.IMREAD_UNCHANGED)
        # traverse the submatrix that will hold the digit
        for y in range(DIGIT_OFFSET_H[0], DIGIT_OFFSET_H[1]):
            # compute effective width boundaries according to digit position,
            # with 1 extra pixel as offset
            start_x = (DIGIT_OFFSET_W[0] + digit*dw) + 1
            end_x = (DIGIT_OFFSET_W[1] + digit*dw) + 1
            for x in range(start_x, end_x):
                # if current pixel is not transparent then substitute the color vector
                if current_digit[y - DIGIT_OFFSET_H[0]][x - start_x][3] > 0:
                    for color in range(3):
                        img[y][x][color] = current_digit[y - DIGIT_OFFSET_H[0]][x - start_x][color]
    return img

def process_image(path_to_img, days):
    img = cv2.imread(path_to_img) 
    overlay = cv2.imread("./assets/overlay.png", cv2.IMREAD_UNCHANGED)
    if round(get_ar(img), 1) != round(ASPECT_RATIO, 1):
        img = crop(img)
    if img.shape[1 : 2] != RESOLUTION_SIZE:
        img = shrink(img)        
    img = apply_overlay(img, overlay)
    img = set_days(img, days)
    cv2.imwrite(path_to_img, img)