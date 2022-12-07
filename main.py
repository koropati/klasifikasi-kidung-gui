from gui.gui import MyGUI, MySettingGUI
import csv
import pandas as pd

splitDuration = 0
shiftDistance = 0
dbTreshold = 0
inputModel = ""
extractFeature = ""

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
            sg.popup('Klasifikasi Kidung', 'Version 1.0', 'PySimpleGUI rocks...')
        if event == "Lihat Pengaturan":
            splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel = readSettingValue("setting.csv")
            sg.popup('Split Duration (second): {}\nShift Distance (second): {}\n dB Treshold: {}\nExtract Feature Method: {}\n Input Model: {}'.format(splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel))
        if event == "Ubah Pengaturan":
            settingWindow(splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel)
            
    
    window.close()

if __name__ == '__main__':
    main()