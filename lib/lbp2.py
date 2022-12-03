import cv2
import numpy as np
from skimage.feature import local_binary_pattern
from skimage.measure import block_reduce


class LBP2(object):
    def __init__(self, image, ):
        self.img = image

    def extract(self):
        lbp = local_binary_pattern(self.img, 8*3, 3, 'default')
        arrLbp = np.array(lbp)
        arrPolling = block_reduce(arrLbp, (4,4), np.mean)
        feature = list(arrPolling.flatten(order='C'))
        return feature