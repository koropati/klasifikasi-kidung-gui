import librosa
import numpy as np
import soundfile as sf
import os


class CleanAudio(object):
    def __init__(self, audioInputPath, audioOutputDir, dbTreshold, duration, shiftDistance):
        self.audio, self.sr = librosa.load(audioInputPath, sr=8000, mono=True)
        self.audioInput = audioInputPath
        self.audioOutputDir = audioOutputDir
        self.dbTreshold = dbTreshold
        self.duration = duration  # in second
        self.shiftDistance = shiftDistance  # in second
        self.className = audioInputPath.split("\\")[-1].split(".")[0]
        self.counterLabel = 1
        self.bufferTimeDuration = self.duration * self.sr # set panjang music = durasi (detik) X sample rate (Hz)
        self.bufferSiftDistance = self.shiftDistance * self.sr # set panjang sift distance = durasi (detik) X sample rate (Hz)

    def extract(self):
        # remove all silent with treshold value
        clips = librosa.effects.split(self.audio, top_db=self.dbTreshold)
        # combine all audio without silent data
        wav_data = []
        for c in clips:
            # print(c)
            data = self.audio[c[0]: c[1]]
            wav_data.extend(data)

        # split to n second duration with shiftDistance duration
        lengthDuration = librosa.get_duration(y=np.array(wav_data), sr=self.sr) #return duration in seconds

        loopingLength = int(((self.duration * ((int(lengthDuration) /
                            self.duration)-1)) + self.shiftDistance)/self.shiftDistance)
        # memotong dari depan ke belakang
        indexStart = 0
        for i in range(loopingLength):
            outPath = self.audioOutputDir + "\\" + \
                self.className + str(self.counterLabel) + ".wav"
            print("OUTPUT: {}".format(outPath))
            print("Indext Start: {}".format(int(indexStart)))
            print("Indext End: {}".format(int(indexStart+self.bufferTimeDuration)))
            split_audio = wav_data[int(indexStart):int(
                indexStart+self.bufferTimeDuration)]
            if os.path.exists(outPath):
                os.remove(outPath)
            sf.write(outPath, split_audio, self.sr)
            # librosa.output.write_wav(outPath, split_audio, self.sr)
            indexStart += self.bufferSiftDistance
            self.counterLabel += 1

        # memotong dari belakang ke depan
        indexEnd = lengthDuration * self.sr
        for i in range(loopingLength):
            outPath = self.audioOutputDir + "\\" + \
                self.className + str(self.counterLabel) + ".wav"
            print("OUTPUT: {}".format(outPath))
            print("Indext Start: {}".format(
                int((indexEnd-self.bufferTimeDuration))))
            print("Indext End: {}".format(int(indexEnd)))
            split_audio = wav_data[int(
                (indexEnd-self.bufferTimeDuration)):int(indexEnd)]
            if os.path.exists(outPath):
                os.remove(outPath)
            sf.write(outPath, split_audio, self.sr)
            # librosa.output.write_wav(outPath, split_audio, self.sr)
            indexEnd -= self.bufferSiftDistance
            self.counterLabel += 1
