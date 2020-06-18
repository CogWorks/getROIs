import os
import pandas as pd

from ...DataClasses.GazeLog import GazeLog

class GazeParser:
    def __init__(self):
        pass

    # This is a parser function that can parse 'seperated value' files (Ex: csv, tsv)
    # Parameters:
    #   gazeFile: String for the absolute path to the file
    #   fileExtension: String value for the type of files to read (Ex: '.tsv', '.csv') 
    #   delimeter: string for the character separating the values (Ex: '\t' for tab-separated values)
    #   colNames: Names of columns (list) in the file, corresponding to the data [should maintain order]
    def parse(self, gazeFile, fileExtension, delimeter, colNames):
        if (gazeFile.endswith(fileExtension)):
            fileContent = pd.read_csv(gazeFile, sep=delimeter)
            gazeData = GazeLog()
            gazeData.subjectID = fileContent[colNames[0]][0]
            gazeData.date = fileContent[colNames[2]][0]
            gazeData.startTime = fileContent[colNames[2]][0]
            gazeData.timeStamp = fileContent[colNames[3]].tolist()
            gazeData.gazeX = fileContent[colNames[4]].tolist()
            gazeData.gazeY = fileContent[colNames[5]].tolist()
            gazeData.gazeZ = fileContent[colNames[6]].tolist()
            gazeData.gazeClass = fileContent[colNames[7]].tolist()
        else:
            print("Could not read file: ", gazeFile, ".")
            return None

        return gazeData