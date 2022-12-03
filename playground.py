
from lib.mode import Mode
from cmd.prediction import Prediction

def main():
    oudioInput = "test.wav"
    dbTreshold = 10
    splitDuration = 5
    shiftDistanceDuration = 2
    typeExtractFeature = "hog"
    model = "model.pkl"
    pred = Prediction(oudioInput, dbTreshold, splitDuration, shiftDistanceDuration, typeExtractFeature, model)
    pred.predict()
    
if __name__ == '__main__':
    main()
