import numpy as np
import pandas as pd
import statistics

# Class untuk mencari data modus dalam file csv

class Mode(object):
    def __init__(self, inputPathCSV):
        self.inputPathCSV = inputPathCSV
        self.data = pd.read_csv(inputPathCSV, sep=',', header=None)
        self.dataTranspose = self.data.T                                                   
        self.myArray = list(self.dataTranspose.values[0])
        self.myClass = list(dict.fromkeys(self.myArray))
        self.accuracyPerClass = [0] * len(self.myClass)
        self.totalData = len(self.myArray)

    def calculate(self):
        # finalData = list([])
        for i in range(len(self.myClass)):
            self.accuracyPerClass[i] = self.myArray.count(self.myClass[i])/self.totalData
        
        # dictionary of lists  
        dictFinalData = {'class_name': self.myClass, 'accuracy': self.accuracyPerClass}
        
        # print("mode :", statistics.mode(self.myArray))
        # print("class :", self.myClass)
        # print("Accuracy per class :", self.accuracyPerClass)
        
        return statistics.mode(self.myArray), dictFinalData
        
        
        
        