import librosa
import numpy as np
import soundfile as sf
import shutil
import os


class Augmented(object):
    def __init__(self, inputPath, outputPath):
        self.x, self.sr = librosa.load(inputPath)
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.className = inputPath.split("\\")[-1].split(".")[0]
        self.fullOutputPath = outputPath + inputPath.split("\\")[-1]

    def pitchAndSpeed(self):
        outPath = self.outputPath + self.className + "_AugPS.wav"
        yPitchSpeed = self.x
        # you can change low and high here
        lengthChange = np.random.uniform(low=0.8, high=1)
        speed_fac = 1.0 / lengthChange
        tmp = np.interp(np.arange(0, len(yPitchSpeed), speed_fac),
                        np.arange(0, len(yPitchSpeed)), yPitchSpeed)
        minlen = min(yPitchSpeed.shape[0], tmp.shape[0])
        yPitchSpeed *= 0
        yPitchSpeed[0:minlen] = tmp[0:minlen]
        return outPath, yPitchSpeed, self.sr

    def pitchOnly(self):
        outPath = self.outputPath + self.className + "_AugPO.wav"
        yPitch = self.x
        binsPerOctave = 12
        pitchPm = 2
        pitchChange = pitchPm * 2*(np.random.uniform())
        yPitch = librosa.effects.pitch_shift(yPitch.astype(
            'float64'), sr=self.sr, n_steps=pitchChange, bins_per_octave=binsPerOctave)
        return outPath, yPitch, self.sr

    def speedOnly(self):
        outPath = self.outputPath + self.className + "_AugSO.wav"
        ySpeed = self.x
        speedChange = np.random.uniform(low=0.9, high=1.1)
        tmp = librosa.effects.time_stretch(
            ySpeed.astype('float64'), rate=speedChange)
        minlen = min(ySpeed.shape[0], tmp.shape[0])
        ySpeed *= 0
        ySpeed[0:minlen] = tmp[0:minlen]
        return outPath, ySpeed, self.sr

    def valueAugmented(self):
        outPath = self.outputPath + self.className + "_AugV.wav"
        yAug = self.x
        dynChange = np.random.uniform(low=1.5, high=3)
        yAug = yAug * dynChange
        return outPath, yAug, self.sr

    def distributionNoise(self):
        outPath = self.outputPath + self.className + "_AugDN.wav"
        yNoise = self.x
        # you can take any distribution from https://docs.scipy.org/doc/numpy-1.13.0/reference/routines.random.html
        noiseAmp = 0.005*np.random.uniform()*np.amax(yNoise)
        yNoise = yNoise.astype('float64') + noiseAmp * \
            np.random.normal(size=yNoise.shape[0])
        return outPath, yNoise, self.sr

    def randomShifting(self):
        outPath = self.outputPath + self.className + "_AugRS.wav"
        yShift = self.x
        timeShiftFac = 0.2 * 2*(np.random.uniform()-0.5)  # up to 20% of length
        start = int(yShift.shape[0] * timeShiftFac)
        if (start > 0):
            yShift = np.pad(yShift, (start, 0), mode='constant')[
                0:yShift.shape[0]]
        else:
            yShift = np.pad(yShift, (0, -start),
                            mode='constant')[0:yShift.shape[0]]
        return outPath, yShift, self.sr

    def applyHpss(self):
        outPath = self.outputPath + self.className + "_AugAH.wav"
        yHpss = librosa.effects.hpss(self.x.astype('float64'))
        return outPath, yHpss[1], self.sr

    def shiftSilentToRight(self):
        outPath = self.outputPath + self.className + "_AugSS.wav"
        sampling = self.x[(self.x > 200) | (self.x < -200)]
        shiftedSilent = sampling.tolist(
        )+np.zeros((self.x.shape[0]-sampling.shape[0])).tolist()
        return outPath, shiftedSilent, self.sr

    def stretching(self):
        outPath = self.outputPath + self.className + "_AugSt.wav"
        inputLength = len(self.x)
        streching = self.x
        streching = librosa.effects.time_stretch(
            streching.astype('float'), rate=1.1)
        if len(streching) > inputLength:
            streching = streching[:inputLength]
        else:
            streching = np.pad(
                streching, (0, max(0, inputLength - len(streching))), "constant")
        return outPath, streching, self.sr

    def create(self):
        if os.path.exists(self.fullOutputPath):
            os.remove(self.fullOutputPath)
        shutil.copy(self.inputPath, self.fullOutputPath)

        outDir, data, sr = self.pitchAndSpeed()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        outDir, data, sr = self.pitchOnly()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        outDir, data, sr = self.speedOnly()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        outDir, data, sr = self.valueAugmented()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        outDir, data, sr = self.distributionNoise()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        outDir, data, sr = self.randomShifting()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        outDir, data, sr = self.applyHpss()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)

        # outDir, data, sr = self.shiftSilentToRight()
        # if os.path.exists(outDir):
        #     os.remove(outDir)
        # print("Writting... {}".format(outDir))
        # sf.write(outDir, data, sr)

        outDir, data, sr = self.stretching()
        if os.path.exists(outDir):
            os.remove(outDir)
        print("Writting... {}".format(outDir))
        sf.write(outDir, data, sr)
