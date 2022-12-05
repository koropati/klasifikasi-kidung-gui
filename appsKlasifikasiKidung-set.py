"""
Perlengkapan
1. Package PySimpleGUI, numpy, openCV, PIL, dan tensorflow 2.8.0
2. Bekerja di OS Windows
3. Pyhton 3.8

Keterangan
# 1. Tempatkan pada folder yang sama dengan code metricsByGusYudha
# 2. Buat folder datasetAerialAreaSawah yang di dalamnya berisi folder trainset, validationset, dan testset
# 3. Run Kode splitingDatasetByGusYudha kemudian hasil dari code program dimasukan ke masing-masing folder (trainset, validationset, dan testset)
# 4. Run Kode Program
"""


import PySimpleGUI as sg
import os.path
import io
import cv2
import time as waktu
import matplotlib.pyplot as plt
import numpy as np

sg.theme('darkblue12')
updateOutput = "variabel ini dipakai untuk nampung nama file hasil segmentasi sementara"


panjangCitra = 512
lebarCitra = 512


# def read_image(lokasi):
#     x = cv2.imread(lokasi, cv2.IMREAD_COLOR)
#     x = cv2.resize(x, (panjangCitra, lebarCitra))
#     x = x/255.0
#     x = x.astype(np.float32)
#     return x


# def read_imagePIL(lokasi, kondisi):
#     inputCitra = WaveObject.open(lokasi)    
#     tampilan = io.BytesIO()
#     inputCitra.save(tampilan, format="WAV")
#     tampilanPIL(tampilan, kondisi)


def TampilanWindow(jenis):
    if jenis == 1:
        jendelaBacaDataset = [
            [sg.HorizontalSeparator(), ],
            [sg.Text("Buka Folder Original Dataset"), ],
            [sg.In(size=(50, 1), enable_events=True,
                   key="FolderDataset"), sg.FolderBrowse(), ],
            [sg.Text("Pilih Dataset dari List"), ],
            [sg.Listbox(values=[], enable_events=True,
                        size=(50, 25), key="ListDataset"), ],            
        ]
        return jendelaBacaDataset
    elif jenis == 2:
        jendelaProsesKlasifikasi = [
            [sg.HorizontalSeparator(), ],
            [sg.Button("Proses Klasifikasi", size=(20, 1),
                       enable_events=True, key="mulaiKlasifikasi")],
            [sg.Text(size=(20, 1), key="Akurasi"), ],
            [sg.Text(size=(20, 1), key="WaktuKlasifikasi"), ],
            [sg.HorizontalSeparator(), ],
            [sg.Text("Lirik Kidung")],
            [sg.Image(key="previewInputDatasest")],
            # [sg.HorizontalSeparator(), ],
        ]
        return jendelaProsesKlasifikasi   


layout = [[
    sg.Column(TampilanWindow(1)),
    sg.VSeperator(),
    sg.Column(TampilanWindow(2)), ]
]


def MainRun():
    window["Akurasi"].update("Akurasi      : 0.0000")
    window["WaktuKlasifikasi"].update("Waktu       : 0.00s")


window = sg.Window(
    "Aplikasi Klasifikasi Kidung Bali", layout).Finalize()
window.Maximize()
MainRun()


while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "FolderDataset":
        folder = values["FolderDataset"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".jpg", ".wav"))
        ]
        window["ListDataset"].update(fnames)

    elif event == "ListDataset":
        try:
            print("do an action here to select your wav audio")
        except:
            pass
    
    elif event == "mulaiKalsifikasi":
        try:

            if (sesiBaru == 1):
                waktuMulai = waktu.time()
                """ Load Dataset .... """
                x = read_image(filenameCitra)
                y, y2 = read_mask(filenameMask)
                outputMask = y2

                """ Proses Prediksi """
                yTebak = model.predict(np.expand_dims(x, axis=0))[0]
                yTebak = yTebak > 0.5
                yTebak = yTebak.astype(np.int32)
                yTebak = np.squeeze(yTebak, axis=-1)
                outputCitra = yTebak

                """ Flatternisasi Array """
                y = y.flatten()
                yTebak = yTebak.flatten()

                waktuBerhenti = waktu.time()

                """ Kalkulasi matriks """
                nilaiAkurasi = accuracy_score(y, yTebak)

                if nilaiAkurasi > 0.999991:
                    nilaif1, nilaiJaccard, nilaiRecall, nilaiPresisi = 1.0, 1.0, 1.0, 1.0
                else:
                    nilaif1 = f1_score(y, yTebak, labels=[
                                       0, 1], average="binary")
                    nilaiJaccard = jaccard_score(
                        y, yTebak, labels=[0, 1], average="binary")
                    nilaiRecall = recall_score(
                        y, yTebak, labels=[0, 1], average="binary")
                    nilaiPresisi = precision_score(
                        y, yTebak, labels=[0, 1], average="binary")

                outputIrisan = np.expand_dims(outputCitra, axis=-1)
                # outputMask = np.expand_dims(outputMask, axis=-1)
                outputCitra = np.expand_dims(outputCitra, axis=-1)

                outputIrisan = np.concatenate(
                    [outputCitra+outputMask, outputCitra+outputMask+1, outputCitra+outputMask], axis=-1) * 85
                # outputMask = np.concatenate([outputMask, outputMask, outputMask], axis=-1)
                outputCitra = np.concatenate(
                    [outputCitra, outputCitra, outputCitra], axis=-1) * 255
                output4Zona = outputCitra
                # cv2.imwrite("hasilSegmentasinya.png", outputCitra)
                # cv2.imwrite("Masknya.png", outputMask)
                # cv2.imwrite("Irisannya.png", outputIrisan)

                sesiBaru = 0

           
            """ Flag """
            th = 21845  # threshold
            
            window["Akurasi"].update(f"Akurasi      : {nilaiAkurasi:0.5f}")            
            window["WaktuSegmentasi"].update(
                f"Waktunya       : {waktuBerhenti - waktuMulai:0.5f}s")
            outputCitra, outputIrisan, output4Zona = Image.open("hasilSegmentasinya.png"), Image.open(
                "Masknya.png"), Image.open("Irisannya.png"), Image.open("hasil4Zona.png").resize((500, 500))

        except:
            pass

window.close()
