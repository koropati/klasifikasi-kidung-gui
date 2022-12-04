
from lib.mode import Mode
from cmd.prediction import Prediction

def main():
    oudioInput = "BimaSuarga_A.wav"
    dbTreshold = 10
    splitDuration = 5
    shiftDistanceDuration = 2
    typeExtractFeature = "hog2"
    model = "model/model_fitur_hog2.pkl"
    pred = Prediction(oudioInput, dbTreshold, splitDuration, shiftDistanceDuration, typeExtractFeature, model)
    winner, modeDictionary = pred.predict()
    
if __name__ == '__main__':
    main()
