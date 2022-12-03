import numpy as np
from csv import writer

def appendListAsRow(namaFile, listOfElem):
	with open(namaFile, 'a+', newline='\n') as writeObj:
		csvWriter = writer(writeObj)
		csvWriter.writerow(listOfElem)

def readCSVFloat(namaFile):
	data = np.genfromtxt(namaFile,delimiter=',', dtype="float")
	return data

def readCSVString(namaFile):
	data = np.genfromtxt(namaFile,delimiter=',', dtype="|U17", autostrip=True)
	return data

def readCSVInt(namaFile):
	data = np.genfromtxt(namaFile,delimiter=',', dtype="int")
	return data