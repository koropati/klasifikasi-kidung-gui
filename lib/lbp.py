import cv2
import numpy as np


class LBP(object):
    def __init__(self, image):
        self.img = image
        self.img = np.asarray(self.img)

    def get_pixel(self, img, center, x, y):
        new_value = 0
        try:
            if img[x][y] >= center:
                new_value = 1
        except:
            pass
        return new_value

    def lbp_calculated_pixel(self, img, x, y):
        center = img[x][y]
        val_ar = []
        val_ar.append(self.get_pixel(img, center, x-1, y+1))     # top_right
        val_ar.append(self.get_pixel(img, center, x, y+1))       # right
        val_ar.append(self.get_pixel(img, center, x+1, y+1))     # bottom_right
        val_ar.append(self.get_pixel(img, center, x+1, y))       # bottom
        val_ar.append(self.get_pixel(img, center, x+1, y-1))     # bottom_left
        val_ar.append(self.get_pixel(img, center, x, y-1))       # left
        val_ar.append(self.get_pixel(img, center, x-1, y-1))     # top_left
        val_ar.append(self.get_pixel(img, center, x-1, y))       # top

        power_val = [1, 2, 4, 8, 16, 32, 64, 128]
        val = 0
        for i in range(len(val_ar)):
            val += val_ar[i] * power_val[i]
        return val

    def reshape_row(self, data_arr):
        row, col = data_arr.shape
        data_out = np.reshape(data_arr, row, order='F')
        return data_out

    def crop_square_4(self, data_array):
        img = data_array
        height, width = img.shape
        img1 = img[0:int(height/2), 0:int(width/2)]
        img2 = img[0:int(height/2), int(width/2):width]
        img3 = img[int(height/2):height, 0:int(width/2)]
        img4 = img[int(height/2):height, int(width/2):width]

        return img1, img2, img3, img4

    def extract(self):
        image_gray = self.img
        height, width = image_gray.shape

        img_lbp = np.zeros((height, width), np.uint8)
        for i in range(0, height):
            for j in range(0, width):
                img_lbp[i, j] = self.lbp_calculated_pixel(image_gray, i, j)

        img1, img2, img3, img4 = self.crop_square_4(img_lbp)

        hist_img1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist_img2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
        hist_img3 = cv2.calcHist([img3], [0], None, [256], [0, 256])
        hist_img4 = cv2.calcHist([img4], [0], None, [256], [0, 256])

        x1 = list(self.reshape_row(hist_img1/sum(sum(hist_img1))))
        x2 = list(self.reshape_row(hist_img2/sum(sum(hist_img2))))
        x3 = list(self.reshape_row(hist_img3/sum(sum(hist_img3))))
        x4 = list(self.reshape_row(hist_img4/sum(sum(hist_img4))))
        feature_vector = []
        feature_vector.extend(x1)
        feature_vector.extend(x2)
        feature_vector.extend(x3)
        feature_vector.extend(x4)

        return feature_vector, img_lbp
