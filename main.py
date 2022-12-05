from gui.gui import MyGUI, MySettingGUI
import csv
splitDuration = 0
shiftDistance = 0
dbTreshold = 0
inputModel = ""

def readSettingValue(csvSetting):
    splitDuration = 0
    shiftDistance = 0
    dbTreshold = 0
    inputModel = ""
    with open(csvSetting, mode='r') as setting:
        csvDataSetting = csv.DictReader(setting)
        for row in csvDataSetting:
            splitDuration = int(row[0])
            shiftDistance = int(row[1])
            dbTreshold = int(row[2])
            inputModel = row[3]
    return splitDuration, shiftDistance, dbTreshold, inputModel

def saveSettingValue(csvSetting, splitDuration, shiftDistance, dbTreshold, inputModel):
    with open(csvSetting, mode='w') as csvDataSetting:
        settingWriter = csv.writer(csvDataSetting, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        settingWriter.writerow([splitDuration, shiftDistance, dbTreshold, inputModel])

def settingWindow(splitDuration, shiftDistance, dbTreshold, inputModel):
    mySettingGUI = MySettingGUI("Pengaturan Klasifikasi Kidung", "darkblue12")
    settingWindow, settingLayout, settingSg = mySettingGUI.initialize()
    
    while True:
        settingEvent, settingValues = settingWindow.read()
        
        settingValues["SplitDuration"] = splitDuration
        settingValues["ShiftDistance"] = shiftDistance
        settingValues["DbTreshold"] = dbTreshold
        settingValues["ModelInput"] = inputModel
        
        if settingEvent == "Exit" or settingEvent == settingSg.WIN_CLOSED or settingEvent == "BatalPengaturan":
            break
        if settingEvent == "SimpanPengaturan":
            print("settingValues['ModelInput'] : ", settingValues['ModelInput'])
            saveSettingValue(csvSetting="setting.csv", splitDuration=settingValues['SplitDuration'],shiftDistance=settingValues['ShiftDistance'],dbTreshold=settingValues['DbTreshold'], inputModel=settingValues['ModelInput'])
            # Update Pengaturan
            settingSg.popup('Berhasil Menyimpan')
            
    settingWindow.close()

def initialValue(window):
    window["PredictedAs"].update("Predicted As  : -")
    window["TimeClassification"].update("Timing Classification : -")

def main():
    # Variabel / Parameter Input
    splitDuration, shiftDistance, dbTreshold, inputModel = readSettingValue("setting.csv")
    
    myGUI = MyGUI("Klasifikasi Kidung", "darkblue12")
    window, layout, sg = myGUI.initialize()
    initialValue(window)
    window.Maximize()
    
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Tentang Aplikasi":      
            sg.popup('Klasifikasi Kidung', 'Version 1.0', 'PySimpleGUI rocks...')
        if event == "Lihat Pengaturan":
            sg.popup('Split Duration (second): {}\nShift Distance (second): {}\n dB Treshold: {}\n Input Model: {}'.format(splitDuration, shiftDistance, dbTreshold, inputModel))
        if event == "Ubah Pengaturan":
            settingWindow(splitDuration, shiftDistance, dbTreshold, inputModel)
            
    
    window.close()

if __name__ == '__main__':
    main()