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
            [sg.Column([[sg.Text("PREDIKSI DATA")]], justification='c')],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Text("Buka File Audio:", font=('Helvetica', 12)), sg.In(size=(35, 1), enable_events=True, key="AudioInput", font=('Helvetica', 12), disabled=True), sg.FileBrowse(file_types=(("Audio Files", "*.wav"),),s=8, font=('Helvetica', 12)),]], justification='c')],
            [sg.Text("")],
            [sg.Column([[sg.Button("Clear Prediksi", key='StopPrediksi', s=20, font=('Helvetica', 14), button_color = ('black','white'), disabled=True), sg.Button("Mulai Prediksi", key='MulaiPrediksi', s=20, font=('Helvetica', 14), button_color = ('black','green'))]], justification='c')],
            [sg.Text("")],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Text("HASIL PREDIKSI")]], justification='c')],
            [sg.HorizontalSeparator(), ],
            [sg.HorizontalSeparator(), ],
            [sg.Text("")],
            [sg.T('ID Proses: ', s=25, justification='l' ,font=('Helvetica', 12)), sg.InputText(key='ProcessID', disabled=True, default_text='-', font=('Helvetica', 12), size=(35, 1))],
            [sg.T('Terprediksi Sebagai Kidung: ', s=25, justification='l', font=('Helvetica', 12)), sg.InputText(key='PredictedAs', disabled=True, default_text='-', font=('Helvetica', 12), size=(35, 1))],
            [sg.T('Waktu Prediksi: ', s=25, justification='l', font=('Helvetica', 12)), sg.InputText(key='TimeClassification', disabled=True, default_text=0, font=('Helvetica', 12), size=(35, 1))],
            [sg.T('Akurasi: ', s=25, justification='l', font=('Helvetica', 12)), sg.InputText(key='PredictedAcuration', disabled=True, default_text=0, font=('Helvetica', 12), size=(35, 1))],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Text("DETAIL PREDIKSI")]], justification='c')],
            [sg.Column([[sg.Multiline(size=(75, 5), key='DetailResult', disabled=True,)]], justification='c')],       
        ]
        
        result = [
            [sg.Column([[sg.Text("FINAL SPECTOGRAM IMAGE LIST")]], justification='c')],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Listbox(values=[], enable_events=True, size=(52, 10), key="ListImageSpectogram")]], justification='c')],
            [sg.Column([[sg.Text("IMAGE PREVIEW")]], justification='c')],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Image(size=(200, 200), key='ImagePreview')]], justification='c')],
        ]
        
        lyricData = [
            [sg.Column([[sg.Text("LIRIK KIDUNG")]], justification='c')],
            [sg.HorizontalSeparator(), ],
            [sg.Column([[sg.Multiline(size=(38, 28), disabled=True, key="lyricData")]], justification='c')],
            ]
        
        layout = [[
            menuHeader,
            sg.vtop(sg.Column(main)),
            sg.VSeperator(),
            sg.vtop(sg.Column(lyricData)),
            sg.VSeperator(),
            sg.vtop(sg.Column(result)),
            ]]
        return layout
    
    def initialize(self):
        return self.Window, self.Layout, sg
                

class MySettingGUI(object):
    def __init__(self, guiName, theme, splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel,):
        self.guiName = guiName
        self.theme = theme
        sg.theme(self.theme)
        self.splitDuration = splitDuration
        self.shiftDistance = shiftDistance
        self.dbTreshold = dbTreshold
        self.inputModel = inputModel
        self.extractFeature = extractFeature
        self.Layout = self.SettingLayout(self.splitDuration, self.shiftDistance, self.dbTreshold, self.extractFeature, self.inputModel)
        self.Window = sg.Window(self.guiName, self.Layout,use_custom_titlebar=True, modal=True)
    
    def SettingLayout(self, splitDuration, shiftDistance, dbTreshold, extractFeature, inputModel):
        buttonSetting = [[sg.Button('Batal', key='BatalPengaturan', s=8, button_color="tomato"), sg.Button("Simpan", bind_return_key=True, key='SimpanPengaturan', s=8)]]
        setting = [
            [sg.HorizontalSeparator(), ],
            [sg.T('Split Duration (second): ', s=20, justification='r'), sg.InputText(key='SplitDuration', default_text=splitDuration)],
            [sg.T('Shift Distance (second): ', s=20, justification='r'), sg.InputText(key='ShiftDistance', default_text=shiftDistance)],
            [sg.T('dB Treshold   (integer): ', s=20, justification='r'), sg.InputText(key='DbTreshold', default_text=dbTreshold)],
            [sg.T('Extract Feature Method: ', s=20, justification='r'), sg.Combo(['hog','hog2','lbp', 'lbp2','combine2','combine3','glcm','glcm2','combine4','combine5','combine6','combine7'],default_value=extractFeature,key='ExtractMethod')],
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