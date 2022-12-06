import PySimpleGUI as sg

class MyGUI(object):
    def __init__(self, guiName, theme):
        self.guiName = guiName
        self.theme = theme
        sg.theme(self.theme)
        self.Layout = self.MainLayout()
        self.Window = sg.Window(self.guiName, self.Layout, use_custom_titlebar=True).Finalize()
        
    def MainLayout(self):
        menu_def = [['Halaman Utama'],      
                ['Pengaturan', ['Ubah Pengaturan','Lihat Pengaturan']],      
                ['Bantuan', 'Tentang Aplikasi'], ] 
        menuHeader = [[sg.Menu(menu_def, key='-MENU-', text_color='black')],]
        main = [
            [sg.Text("Buka File Audio:"), sg.In(size=(50, 1), enable_events=True, key="AudioInput"), sg.FolderBrowse(),],
            [sg.Text("")],
            [sg.Column([[sg.Button("Mulai Prediksi", key='MulaiPrediksi', s=20)]], justification='c')],
            [sg.Text("")],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Text("HASIL PREDIKSI")]], justification='c')],
            [sg.HorizontalSeparator(), ],
            [sg.HorizontalSeparator(), ],
            [sg.Text("")],
            [sg.T('ID Proses: ', s=25, justification='l'), sg.InputText(key='ProcessID', disabled=True, default_text='-')],
            [sg.T('Terprediksi Sebagai Kidung: ', s=25, justification='l'), sg.InputText(key='PredictedAs', disabled=True, default_text='-')],
            [sg.T('Waktu Prediksi: ', s=25, justification='l'), sg.InputText(key='TimeClassification', disabled=True, default_text=0)],
            [sg.T('Akurasi: ', s=25, justification='l'), sg.InputText(key='PredictedAcuration', disabled=True, default_text=0)],          
        ]
        result = [
            [sg.Text("Final Spectogram Image List"), ],
            [sg.Listbox(values=[], enable_events=True, size=(50, 25), key="ListImageSpectogram"), ]
        ]
        
        layout = [[
            menuHeader,
            sg.vtop(sg.Column(main)),
            sg.VSeperator(),
            sg.vtop(sg.Column(result)),
            ]]
        return layout
    
    def initialize(self):
        return self.Window, self.Layout, sg
                

class MySettingGUI(object):
    def __init__(self, guiName, theme, splitDuration, shiftDistance, dbTreshold, inputModel):
        self.guiName = guiName
        self.theme = theme
        sg.theme(self.theme)
        self.splitDuration = splitDuration
        self.shiftDistance = shiftDistance
        self.dbTreshold = dbTreshold
        self.inputModel = inputModel
        self.Layout = self.SettingLayout(self.splitDuration, self.shiftDistance, self.dbTreshold, self.inputModel)
        self.Window = sg.Window(self.guiName, self.Layout,use_custom_titlebar=True, modal=True)
    
    def SettingLayout(self, splitDuration, shiftDistance, dbTreshold, inputModel):
        buttonSetting = [[sg.Button('Batal', key='BatalPengaturan', s=8, button_color="tomato"), sg.Button("Simpan", bind_return_key=True, key='SimpanPengaturan', s=8)]]
        setting = [
            [sg.HorizontalSeparator(), ],
            [sg.T('Split Duration (second): ', s=20, justification='r'), sg.InputText(key='SplitDuration', default_text=splitDuration)],
            [sg.T('Shift Distance (second): ', s=20, justification='r'), sg.InputText(key='ShiftDistance', default_text=shiftDistance)],
            [sg.T('dB Treshold   (integer): ', s=20, justification='r'), sg.InputText(key='DbTreshold', default_text=dbTreshold)],
            [sg.T('Input Model     (pickle file): ', s=20, justification='r'), sg.In(size=(36, 1), enable_events=True, key="ModelInput", justification='r', default_text=inputModel), sg.FileBrowse()],
            [sg.HorizontalSeparator(), ],
            [sg.HorizontalSeparator(), ],
            [sg.Column(buttonSetting, expand_x=True, element_justification='right')],
            [sg.HorizontalSeparator(), ],
        ]
        layout = [[
            sg.VSeperator(),
            sg.Column(setting),
            sg.VSeperator(),
            ]]
        return layout
    
    def initialize(self):
        return self.Window, self.Layout, sg