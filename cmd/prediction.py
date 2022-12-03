import librosa
import uuid
import os
import shutil

from lib.preprocessing import CleanAudio
from lib.spectogram import CreateSpectogram, CropImageSpectogram

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
        # Crop Spectogram
        self.cropSpectogram(self.folderSpectogram, self.folderSpectogramCrop, "png")
        
        
        
        
        
        