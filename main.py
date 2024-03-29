from gui.gui import MyGUI, MySettingGUI
from cmd.prediction import Prediction
from helper.delete import deleteLogFile
import csv
import pandas as pd
import uuid
import os, re
import time as waktu

splitDuration = 0
shiftDistance = 0
dbTreshold = 0
inputModel = ""
extractFeature = ""
uuidProcess = ""
listImageSpectogram = []
pathImageSpectogram = ""
folderModel = "model/"
folderLyric = "lyrics/"
pathLyric = ""
isProcessing = False

def readSettingValue(csvSetting):
    df = pd.read_csv(csvSetting)
    splitDuration = df['split_duration'].iloc[0]
    shiftDistance = df['shift_distance'].iloc[0]
    dbTreshold = df['db_treshold'].iloc[0]
    inputModel = df['input_model'].iloc[0]
    extractFeature = df['extract_feature'].iloc[0]
    return splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel

def saveSettingValue(csvSetting, splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel):
    df = pd.read_csv(csvSetting)
    df.loc[0,'split_duration'] = splitDuration
    df.loc[0,'shift_distance'] = shiftDistance
    df.loc[0,'db_treshold'] = dbTreshold
    df.loc[0,'extract_feature'] = extractFeature
    df.loc[0,'input_model'] = inputModel
    
    df.to_csv(csvSetting, index=False)
    return splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel

def settingWindow(splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel):
    mySettingGUI = MySettingGUI("Pengaturan Klasifikasi Kidung", "darkblue12", splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel)
    settingWindow, settingLayout, settingSg = mySettingGUI.initialize()
    
    while True:
        settingEvent, settingValues = settingWindow.read()
        if settingEvent == "Exit" or settingEvent == settingSg.WIN_CLOSED or settingEvent == "BatalPengaturan":
            break
        if settingEvent == "SimpanPengaturan":
            splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel = saveSettingValue(csvSetting="setting.csv", splitDuration=settingValues['SplitDuration'],shiftDistance=settingValues['ShiftDistance'],dbTreshold=settingValues['DbTreshold'], extractFeature=settingValues['ExtractMethod'], inputModel=settingValues['ModelInput'])
            # Update Pengaturan
            settingSg.popup('Berhasil Menyimpan')
            
    settingWindow.close()
    
def readFolderFileList(inputpath):
    result = []
    for path in os.listdir(inputpath):
        # check if current path is a file
        if os.path.isfile(os.path.join(inputpath, path)):
            result.append(path)
    return result

def main():
    # Variabel / Parameter Input
    splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel = readSettingValue("setting.csv")
    
    myGUI = MyGUI("Klasifikasi Kidung", "darkblue12")
    window, layout, sg = myGUI.initialize()
    # window.Maximize()
    
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Tentang Aplikasi":      
            sg.popup("Klasifikasi Kidung\nGUI Version 1.0\nAyu Ditha Savitri \nNIM: ", title='Tentang Aplikasi')
        if event == "Lihat Pengaturan":
            splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel = readSettingValue("setting.csv")
            sg.popup('Split Duration (second): {}\nShift Distance (second): {}\ndB Treshold: {}\nExtract Feature Method: {}\nInput Model: {}'.format(splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel), title='Pengaturan Klasifikasi')
        if event == "Ubah Pengaturan":
            settingWindow(splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel)
            
        if event == "MulaiPrediksi":
            isProcessing = True
            audioInput = values['AudioInput']
            uuidProcess = str(uuid.uuid4())
            pathImageSpectogram = "img/spectogram-crop/" + uuidProcess + "/"
            if inputModel == "" or extractFeature == "" or splitDuration == 0 or shiftDistance == 0 or dbTreshold == 0 :
                isProcessing = False
                sg.popup("Data Pengaturan masih kosong atau ada data yang tidak valid", "Silahkan cek dan ubah pengaturan pada menu penagturan", "Terimakasih!", title='Kesalahan')
            elif audioInput == "":
                isProcessing = False
                sg.popup("Input Audio Terlebih Dahulu", "Terimakasih!", title='Kesalahan')
            elif os.path.isfile(inputModel) == False:
                isProcessing = False
                sg.popup("Data Model Tidak Ditemukan", "Silahkan ubah pengaturan pada file model input!", title='Kesalahan')
            elif os.path.isfile(audioInput) == False:
                isProcessing = False
                sg.popup("Data Audio Tidak Ditemukan", "Silahkan input audio yang akan di prediksi!", title='Kesalahan')
            else:
                try:
                    window['MulaiPrediksi'].update("Processing...", button_color = ('black','white'), disabled=isProcessing)

                    window['ProcessID'].Update(uuidProcess)
                    
                    # Mulai Prediksi
                    waktuMulai = waktu.time()
                    MyPrediction = Prediction(uuidProcess, audioInput, dbTreshold, splitDuration, shiftDistance, extractFeature, inputModel)
                    winner, winnerAccuracy, detailText, modeDictionary = MyPrediction.predict()
                    waktuBerhenti = waktu.time()
                    isProcessing = False
                    # Selesai Prediksi
                    
                    # Update path lyric
                    pathLyric = folderLyric + winner + ".txt"
                    fileLyric = open(pathLyric, "r")
                    dataLyric = fileLyric.read()
                    fileLyric.close()
                    
                    # Menampilkan Hasil Prediksi
                    window['PredictedAs'].Update(re.sub(r"(\w)([A-Z])", r"\1 \2", winner))
                    window['PredictedAcuration'].Update(winnerAccuracy)
                    window['DetailResult'].Update(detailText)
                    window['TimeClassification'].Update(f"{waktuBerhenti - waktuMulai:0.5f} Detik")
                    listImageSpectogram = readFolderFileList(pathImageSpectogram)
                    window['ListImageSpectogram'].update(listImageSpectogram)
                    window['lyricData'].update(dataLyric)
                    
                    sg.popup("Selesai Melakukan Prediksi, Terprediksi Sebagai : " + winner, title='Sukses')
                except:
                    sg.popup("Terjadi Kesalahan Pada Sistem silahkan cek log data!. Terimakasih!", title='Kesalahan')
                finally:
                    # Aktifkan / Non aktifkan Tombol
                    window['MulaiPrediksi'].update("Mulai Prediksi",button_color = ('black','green'), disabled=isProcessing)
                    window['StopPrediksi'].update(button_color = ('black','red'), disabled=False)
                    
        if event == "ListImageSpectogram":
            selection = values[event]
            if selection:
                itemImage = selection[0]
                window['ImagePreview'].update(filename=pathImageSpectogram+itemImage)
            
        if event == "StopPrediksi":
            try:
                if uuidProcess != "":
                    deleteLogFile(uuidProcess)
                    window['ProcessID'].Update("-")
                    window['PredictedAs'].Update("-")
                    window['TimeClassification'].Update("0")
                    window['PredictedAcuration'].Update("0")
                    window['DetailResult'].Update("")
                    window['ListImageSpectogram'].update("")
                    window['ImagePreview'].update("")
                    window['AudioInput'].update("")
                    window['lyricData'].update("")
                    window['StopPrediksi'].update(button_color = ('black','white'), disabled=True)
                    sg.popup("Sukses Membersihkan Prediksi, Data prediksi lama telah di hapus", title='Sukses')
            except:
                sg.popup("Terjadi Kesalahan, Pada Sistem silahkan cek log data", "Terimakasih!", title='Kesalahan')
    
    window.close()

if __name__ == '__main__':
    main()