import os
import pandas as pd

from ....DataClasses.GazeLog import GazeLog


# This is a parser function that can parse 'seperated value' files (Ex: csv, tsv)
# Parameters:
#   gazeFile: String for the absolute path to the file
#   fileExtension: String value for the type of files to read (Ex: '.tsv', '.csv') 
#   delimeter: string for the character separating the values (Ex: '\t' for tab-separated values)
#   colNames: Names of columns (list) in the file, corresponding to the data [should maintain order]
def parse(gazeFile, fileExtension, delimeter, colNames):
    if (gazeFile.endswith(fileExtension)):
        fileContent = pd.read_csv(gazeFile, sep=delimeter)
        gazeData = GazeLog()
        gazeData.subjectID = fileContent[colNames[0]]
        gazeData.sessionNum = fileContent[colNames[1]]
        if not colNames[2] == None:
            gazeData.gameNum = fileContent[colNames[2]]
        gazeData.timeStamp = fileContent[colNames[3]]
        gazeData.gazeX = fileContent[colNames[4]]
        gazeData.gazeY = fileContent[colNames[5]]
        gazeData.gazeZ = fileContent[colNames[6]]
    else:
        print("Could not read file: ", gazeFile, ".")
        return None

    return gazeData