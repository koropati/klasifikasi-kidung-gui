import PySimpleGUI as sg

class MyGUI(object):
    def __init__(self, guiName, theme):
        self.guiName = guiName
        self.theme = theme
        sg.theme(self.theme)
        self.Layout = self.MainLayout()
        self.Window = sg.Window(self.guiName + " [Main]", self.Layout).Finalize()
        
    def MainLayout(self):
        menu_def = [['Halaman Utama'],      
                ['Pengaturan', ['Ubah Pengaturan','Lihat Pengaturan']],      
                ['Bantuan', 'Tentang Aplikasi'], ] 
        menuHeader = [[sg.Menu(menu_def, key='-MENU-', text_color='black')],]
        main = [
            [sg.HorizontalSeparator(), ],
            [sg.Text("Buka File Audio"), ],
            [sg.In(size=(50, 1), enable_events=True, key="AudioInput"), sg.FolderBrowse(), ],          
        ]
        result = [
            [sg.Text(size=(20, 1), key="PredictedAs"), ],
            [sg.Text(size=(20, 1), key="TimeClassification"),],
        ]
        
        layout = [[
            menuHeader,
            sg.Column(main),
            sg.VSeperator(),
            sg.Column(result),
            ]]
        return layout
    
    def initialize(self):
        return self.Window, self.Layout, sg
                

class MySettingGUI(object):
    def __init__(self, guiName, theme):
        self.guiName = guiName
        self.theme = theme
        sg.theme(self.theme)
        self.Layout = self.SettingLayout()
        self.Window = sg.Window(self.guiName + " [Main]", self.Layout, modal=True)
    
    def SettingLayout(self):
        buttonSetting = [[sg.Button("Simpan", bind_return_key=True, key='SimpanPengaturan'), sg.Button('Batal', key='BatalPengaturan')]]
        setting = [
            [sg.Text("Pengaturan")],
            [sg.Text('Enter Split Duration (second): '), sg.InputText(key='SplitDuration')],
            [sg.Text('Enter Shift Distance (second): '), sg.InputText(key='ShiftDistance')],
            [sg.Text('Enter dB Treshold   (integer): '), sg.InputText(key='DbTreshold')],
            [sg.Text('Input Model     (pickle file): '), sg.In(size=(25, 1), enable_events=True, key="ModelInput"), sg.FileBrowse()],
            [sg.Column(buttonSetting, expand_x=True, element_justification='right')],
        ]
        return setting
    
    def initialize(self):
        return self.Window, self.Layout, sg