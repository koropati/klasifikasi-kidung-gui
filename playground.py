
from lib.mode import Mode
from cmd.prediction import Prediction
import uuid

def main():
    oudioInput = "BimaSuarga_A.wav"
    dbTreshold = 10
    splitDuration = 5
    shiftDistanceDuration = 2
    typeExtractFeature = "hog2"
    model = "model/model_fitur_hog2.pkl"
    pred = Prediction(str(uuid.uuid4()),oudioInput, dbTreshold, splitDuration, shiftDistanceDuration, typeExtractFeature, model)
    winner, winnerAccuracy, detailText, modeDictionary = pred.predict()
    
if __name__ == '__main__':
    main()
