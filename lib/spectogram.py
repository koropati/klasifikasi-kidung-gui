import librosa
import matplotlib.pyplot as plt
import librosa.display
import cv2
import numpy as np


class CreateSpectogram(object):
    def __init__(self, audioPath, imagePath):
        self.x, self.sr = librosa.load(audioPath)
        self.audioPath = audioPath
        self.imagePath = imagePath

    def create(self):
        myDPI = 90
        widthInch = (576/myDPI)
        heightInch = (432/myDPI)
        librosa.load(self.audioPath, sr=None)
        X = librosa.stft(self.x)
        Xdb = librosa.amplitude_to_db(abs(X))
        fig, ax = plt.subplots(1, figsize=(widthInch, heightInch))
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis('off')
        librosa.display.specshow(Xdb, sr=self.sr)
        ax.axis('off')
        fig.savefig(self.imagePath, dpi=myDPI, frameon='false')
        plt.close()


class CropImageSpectogram(object):
    def __init__(self, inputPath, outPath):
        self.inputPath = inputPath
        self.outPath = outPath
        self.img = cv2.imread(self.inputPath)
        self.imgGray = cv2.imread(self.inputPath, cv2.IMREAD_GRAYSCALE)
        self.hsvImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

    def crop(self):
        (_, maskingData) = cv2.threshold(self.imgGray, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        white_pt_coords = np.argwhere(maskingData)
        min_y = min(white_pt_coords[:, 0])
        min_x = min(white_pt_coords[:, 1])
        max_y = max(white_pt_coords[:, 0])
        max_x = max(white_pt_coords[:, 1])
        crop = self.img[min_y:max_y, min_x:max_x]
        resized = cv2.resize(crop, (576, 216), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.outPath, resized)
    
    def cropOrange(self): 
        bound_lower = np.array([0, 100, 45])
        bound_upper = np.array([225, 250, 255])
        maskOrange = cv2.inRange(self.hsvImg, bound_lower, bound_upper)
        maskingData = np.invert(maskOrange)
        white_pt_coords=np.argwhere(maskingData)
        min_y = min(white_pt_coords[:,0])
        min_x = min(white_pt_coords[:,1])
        max_y = max(white_pt_coords[:,0])
        max_x = max(white_pt_coords[:,1])
        crop = self.img[min_y:max_y, min_x:max_x]
        resized = cv2.resize(crop, (576, 216), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.outPath, resized)
        
    def cropROI(self):
        # 287
        height, width, _ = self.img.shape
        min_y = 287
        min_x = 0
        max_y = height
        max_x = width
        crop = self.img[min_y:max_y, min_x:max_x]
        resized = cv2.resize(crop, (576, 216), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.outPath, resized)
