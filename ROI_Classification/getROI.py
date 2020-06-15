# Parameters:
gazeData_fileType = ".tsv"
gazeData_delimeter = "\t"
gazeData_colNames = []
gameData_colNames = []

# Get gaze data
# Get SID, gameNo and SessNo
# Fetch corresponding game-data from SQL
# For CTWC19: Fetch time-sync files
# Align timings
# Run ROI analysis code

import os

from ROI_Library.Parsers.GazeParsers import Tobii_gazeTools_CSV_Parser as gazeParser
from ROI_Library.Parsers.GameParsers import Meta2_SQL_Parser as gameParser


# Parameters:
#   sourcePath: Directory containing all the source files [should be a flat directory]
def getClassifications(sourcePath):
    for inFile in os.scandir(sourcePath):
        if (inFile.is_file() and inFile.path.endswith(gazeData_fileType)):
            print("Processing game corresponding to file: ", inFile.path.split("/")[-1])
            gazeData = gazeParser.parse(inFile.path, gazeData_fileType, gazeData_delimeter, gazeData_colNames)
            if gazeData == None:
                continue
            gameData = gameParser.parse(gameData_colNames)
            if gameData == None:
                continue