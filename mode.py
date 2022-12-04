
from lib.mode import Mode
# from cmd.prediction import Prediction

def main():
    inputCSV = "data/mode/e28b969e-53a0-4b01-8711-a9c18e61ebab/hog2.csv"
    myMode = Mode(inputCSV)
    winnerClass, dictinaryData = myMode.calculate()
    print("Winner is : ", winnerClass)
    print("dictionary: ", dictinaryData)
    
if __name__ == '__main__':
    main()
