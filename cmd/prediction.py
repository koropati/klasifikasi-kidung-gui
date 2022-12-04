import librosa
import uuid
import os
import shutil
import cv2
import numpy as np
import sys
import pickle
import pandas as pd

from pydoc import classname
from skimage.feature import hog

from lib.preprocessing import CleanAudio
from lib.spectogram import CreateSpectogram, CropImageSpectogram
from lib.hog import HOG
from lib.lbp import LBP
from lib.lbp2 import LBP2
from lib.glcm import GLCM, GLCM2
from lib.mode import Mode
from lib.csv import appendListAsRow, readCSVFloat

class Prediction(object):
    def __init__(self, oudioInput, dbTreshold, splitDuration, shiftDistanceDuration, typeExtractFeature, model):
        self.fileName, self.fileExtensionInput = os.path.splitext(oudioInput)
        self.fileNameInput = self.fileName.rsplit('/', 1)[-1]
        self.audio, self.sr = librosa.load(oudioInput, sr=8000, mono=True)
        self.oudioInput = oudioInput
        self.dbTreshold = dbTreshold
        self.splitDuration = splitDuration  # in second
        self.shiftDistanceDuration = shiftDistanceDuration  # in second
        self.typeExtractFeature = typeExtractFeature
        self.bufferTimeDuration = self.splitDuration * self.sr # set panjang music = durasi (detik) X sample rate (Hz)
        self.bufferSiftDistance = self.shiftDistanceDuration * self.sr # set panjang sift distance = durasi (detik) X sample rate (Hz)
        self.model = model #model file .pkl
        self.processID = str(uuid.uuid4())
        
        self.folderAudioInput = "audio/input/" + self.processID + "/"
        self.folderAudioInputCleanSplit = "audio/clean-split/" + self.processID + "/"
        self.folderSpectogram = "img/spectogram/" + self.processID + "/"
        self.folderSpectogramCrop = "img/spectogram-crop/" + self.processID + "/"
        self.folderMode = "data/mode/" + self.processID + "/"
        self.folderPredicted = "data/predicted/" + self.processID + "/"
        self.folderVector = "data/vector/" + self.processID + "/"
    
    def createSpectogram(self, src, dst, extension):
        print("[CREATING SPECTOGRAM]")
        if not os.path.exists(dst):
            os.makedirs(dst)

        for root, dirs, files in os.walk(src):
            
            for name in files:
                fullPathIn = root + os.sep + name
                
                classImage = name.split("_")
                folderClass = dst + os.sep
                nameOut = name.split(".")
                fullPathOut = folderClass + os.sep + nameOut[0] + "." + extension
                if not os.path.exists(folderClass):
                    os.makedirs(folderClass)
            
                if os.path.exists(fullPathOut):
                    os.remove(fullPathOut)
                
                
                mySpectogram = CreateSpectogram(fullPathIn, fullPathOut)
                mySpectogram.create()
                print("Created Image : {}".format(fullPathOut))
        print("Done!")
    
    def cropSpectogram(self, src, dst, extension):
        print("[CROPPING SPECTOGRAM]")
        if not os.path.exists(dst):
            os.makedirs(dst)

        for root, dirs, files in os.walk(src):
            
            for name in files:
                fullPathIn = root + os.sep + name
                
                classImage = name.split("_")
                folderClass = dst + os.sep
                nameOut = name.split(".")
                fullPathOut = folderClass + os.sep + nameOut[0] + "." + extension
                if not os.path.exists(folderClass):
                    os.makedirs(folderClass)
            
                if os.path.exists(fullPathOut):
                    os.remove(fullPathOut)
                
                
                mySpectogram = CropImageSpectogram(fullPathIn, fullPathOut)
                mySpectogram.cropROI()
                print("Created Image : {}".format(fullPathOut))
        print("Done!")
    
    def generateCSVFeature(self, src, dst, methodFeature):
        print("[EXTRACTING FEATURE]")
        nameFileOut = self.folderVector + methodFeature + ".csv"
        if not os.path.exists(dst):
            os.makedirs(dst)

        if os.path.exists(nameFileOut):
            os.remove(nameFileOut)

        for root, dirs, files in os.walk(src):
            for name in files:
                vectorFeature = []
                fullPathIn = root + os.sep + name

                img_colour = cv2.imread(fullPathIn)
                img_gray = cv2.imread(fullPathIn, cv2.IMREAD_GRAYSCALE)

                if methodFeature == 'hog':
                    myHOG = HOG(img_gray, 16, 8)
                    hogVector, _ = myHOG.extract()
                    vectorFeature.extend(hogVector)
                elif methodFeature == 'hog2':
                    myHOG2 = hog(img_gray, orientations=8, pixels_per_cell=(
                        16, 16), cells_per_block=(1, 1), visualize=False, feature_vector=True)
                    vectorFeature.extend(list(myHOG2))
                elif methodFeature == 'lbp':
                    # skip
                    myLBP = LBP(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                elif methodFeature == 'lbp2':
                    myLBP = LBP2(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                elif methodFeature == 'combine2':
                    myHOG2 = hog(img_gray, orientations=8, pixels_per_cell=(
                        16, 16), cells_per_block=(1, 1), visualize=False, feature_vector=True)
                    vectorFeature.extend(list(myHOG2))
                    myLBP = LBP2(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                elif methodFeature == 'combine3':
                    myHOG = HOG(img_gray, 16, 8)
                    hogVector, _ = myHOG.extract()
                    vectorFeature.extend(hogVector)
                    myLBP = LBP2(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                elif methodFeature == 'glcm':
                    glcmVector = GLCM(img_gray).extract()
                    vectorFeature.extend(glcmVector)
                elif methodFeature == 'glcm2':
                    glcmVector = GLCM2(img_gray, img_colour).extract()
                    vectorFeature.extend(glcmVector)
                elif methodFeature == 'combine4':
                    myHOG = HOG(img_gray, 16, 8)
                    hogVector, _ = myHOG.extract()
                    vectorFeature.extend(hogVector)
                    glcmVector = GLCM2(img_gray, img_colour).extract()
                    vectorFeature.extend(glcmVector)
                elif methodFeature == 'combine5':
                    myLBP = LBP2(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                    glcmVector = GLCM2(img_gray, img_colour).extract()
                    vectorFeature.extend(glcmVector)
                elif methodFeature == 'combine6':
                    myHOG = HOG(img_gray, 16, 8)
                    hogVector, _ = myHOG.extract()
                    vectorFeature.extend(hogVector)
                    glcmVector = GLCM(img_gray).extract()
                    vectorFeature.extend(glcmVector)
                elif methodFeature == 'combine7':
                    myLBP = LBP2(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                    glcmVector = GLCM(img_gray).extract()
                    vectorFeature.extend(glcmVector)
                else:
                    # skipp
                    myHOG = HOG(img_gray, 16, 8)
                    hogVector, _ = myHOG.extract()
                    vectorFeature.extend(hogVector)
                    myLBP = LBP(img_gray)
                    lbpVector = myLBP.extract()
                    vectorFeature.extend(lbpVector)
                print("Processed : {}".format(fullPathIn))
                appendListAsRow(nameFileOut, vectorFeature)
        print("Done!")
        
    def predictionVectorCSV(self, dst):
        # Check Path atau lokasi file feature
        csvInput = self.folderVector + self.typeExtractFeature + ".csv"
        if not os.path.exists(csvInput):
            print("File : {} NOT EXIST".format(csvInput))
            sys.exit()
        # dfFeature = pd.read_csv(datasetFeaturePath)
        dfFeature = readCSVFloat(csvInput)
        model = pickle.load(open(self.model, 'rb'))
        result = model.predict(dfFeature)
        finalResult = result.T
        pd.DataFrame(finalResult).to_csv(dst, header=False, index=False)
        print("RESULT: ", finalResult)
    
    def calculateMode(self, dst):
        csvInput = self.folderMode + self.typeExtractFeature + ".csv"
        if not os.path.exists(csvInput):
            print("File : {} NOT EXIST".format(csvInput))
            sys.exit()
        myMode = Mode(csvInput)
        winner, modeDictionary = myMode.calculate()
        dfMode = pd.DataFrame(modeDictionary)
        dfMode.to_excel(dst)
        print("Adudio predicted As: ",winner)
        return winner, modeDictionary
        
        
    def predict(self):
        # Check Folder is exist or not
        if not os.path.exists(self.folderAudioInput):
            os.makedirs(self.folderAudioInput)
        
        if not os.path.exists(self.folderAudioInputCleanSplit):
            os.makedirs(self.folderAudioInputCleanSplit)
        
        if not os.path.exists(self.folderSpectogram):
            os.makedirs(self.folderSpectogram)
            
        if not os.path.exists(self.folderSpectogramCrop):
            os.makedirs(self.folderSpectogramCrop)
            
        if not os.path.exists(self.folderMode):
            os.makedirs(self.folderMode)
            
        if not os.path.exists(self.folderPredicted):
            os.makedirs(self.folderPredicted)
        
        if not os.path.exists(self.folderVector):
            os.makedirs(self.folderVector)
        # End Creatinf folder
        
        # Save Audio user input to folder input
        shutil.copyfile(self.oudioInput, self.folderAudioInput+self.fileNameInput+self.fileExtensionInput)
        
        # Cleaning Audio
        print("[CLEANING AUDIO]")
        audioClean = CleanAudio(self.oudioInput, self.folderAudioInputCleanSplit, self.dbTreshold, self.splitDuration, self.shiftDistanceDuration)
        audioClean.extract()
        # End Cleaning Audio
        
        # Create Spectogram
        self.createSpectogram(self.folderAudioInputCleanSplit, self.folderSpectogram, "png")
        # End Create Spectogram
        
        # Crop Spectogram
        self.cropSpectogram(self.folderSpectogram, self.folderSpectogramCrop, "png")
        # End Croping Spectogram
        
        # Create Feature Extraction
        self.generateCSVFeature(self.folderSpectogramCrop, self.folderVector, self.typeExtractFeature)
        # End Create Feature Extraction
        
        # Predicting All row in Feature Extraction
        self.predictionVectorCSV(self.folderMode+self.typeExtractFeature+".csv")
        # End Predicting All row in Feature Extraction
        
        # Calculate Modus in csv data predicted
        return self.calculateMode(self.folderPredicted+self.typeExtractFeature+".xlsx")
        # Calculate Modus in csv data predicted