import argparse
import os
import shutil

def deleteLogFile(uuid):
    folderAudioCleanSplit = "audio/clean-split/"+uuid
    folderAudioInput = "audio/input/"+uuid
    folderDataMode = "data/mode/"+ uuid
    folderDataPredicted = "data/predicted/"+uuid
    folderDataVector = "data/vector/"+uuid
    folderImgSpectogram = "img/spectogram/"+uuid
    folderImgSpectogramCrop = "img/spectogram-crop/"+uuid
    try:
        shutil.rmtree(folderAudioCleanSplit, ignore_errors=True)
        shutil.rmtree(folderAudioInput, ignore_errors=True)
        shutil.rmtree(folderDataMode, ignore_errors=True)
        shutil.rmtree(folderDataPredicted, ignore_errors=True)
        shutil.rmtree(folderDataVector, ignore_errors=True)
        shutil.rmtree(folderImgSpectogram, ignore_errors=True)
        shutil.rmtree(folderImgSpectogramCrop, ignore_errors=True)
    except:
        print("Error When Deleteing LOG File!")
        
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--inputProcessID', required=True,help='Input UUID / Process ID')
    args = ap.parse_args()
    print("Clearing Log File: ", args.inputProcessID)
    deleteLogFile(args.inputProcessID)
    print("Done!")
    
if __name__ == '__main__':
    main()
