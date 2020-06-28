# Parameters:
gazeData_fileType = ".tsv"
# Parameters:
#   sourcePath: Directory containing all the source files [should be a flat directory]
#   syncFile: If this is set to True it will look for sync files for the games 
#               sync files contain Recording time stamps and their corrsponding system timestamps,
#               in the CTWC19 Data.
gazeData_delimeter = "\t"
gazeData_colNames = ["Participant name", "Recording date", "Recording start time", "Eyetracker timestamp", "x", "y", "Eye position left Z (DACSmm)", "class"]
Event_Identifier = "CTWC19"
gameData_colNames = ["SID", "SessionNum", "GameNum", "Screen_Resolution", "ts", "system_ticks", "board_rep", "zoid_rep"]
sourcePath = "/CogWorks/cwl-data/Active_Projects/Tetris/Workspaces/Banerjee/Gaze_Stuff/R_Files/Gaze_Outputs/CTWC19/"
syncFile = True


# Get gaze data
# Get SID, gameNo and SessNo
# Fetch corresponding game-data from SQL
# For CTWC19: Fetch time-sync files
# Align timings
# Run ROI analysis code


# Import Libraries
import os

from Library.Parsers.GazeParsers.Tobii_gazeTools_CSV_Parser import GazeParser
from Library.Parsers.GameParsers.Meta2_SQL_Parser import GameParser
from Library.Parsers.OtherParsers.CTWC19_SyncFile_Parser import SycnParser
from Library.Utilities.CTWC19_Utils import alignData_GameGaze as align
# from Library.ROI_Codes.GenerateROI import generateROI


def getClassifications():
    count = 0
    gazeParser = GazeParser()
    gameParser = GameParser()
    syncParser = SycnParser("/CogWorks/cwl-data/Active_Projects/Tetris/External_Tournaments/CTWC19/meta-two/")
    # Loop through all gaze files in the directory
    for inFile in os.scandir(sourcePath):
        if (inFile.is_file() and inFile.path.endswith(gazeData_fileType)):
            print("Processing data corresponding to gaze file: \n", inFile.path.split("/")[-1])
            count += 1
            # Parse the gaze file and get gaze object with all information
            gazeData = gazeParser.parse(inFile.path, gazeData_fileType, gazeData_delimeter, gazeData_colNames)
            if gazeData == None:
                continue
            # Get file paths of all experiments corresponding to the gaze file (generally 1)
            experimentFile_paths = syncParser.get_filePath_from_eyetrackerTime(gazeData.timeStamp, gazeData.subjectID)
            if gazeData == None:
                continue
            # elif len(experimentFile_paths)>1:
            #     print("Has more than one associated expeiment:\n", experimentFile_paths)
            # Loop through each experiment
            for path in experimentFile_paths:
                # Get IDs for all games in that experiment
                gameIDs = gameParser.get_gameID_fromFilePath(path, 'gameID', 'CTWC19')
                if gameIDs == None:
                    continue
                for ID in gameIDs:
                    gameData = gameParser.parse(ID, gameData_colNames)
                    if gameData == None:
                        continue
                    # combinedDF = align(gameData, syncParser.get_data_from_path(path), gazeData)
                    # ROIs = generateROI(combinedDF)
            print("Processing ", count, " files complete...")



getClassifications()





def testFunc():
    from Library.Parsers.OtherParsers.CTWC19_SyncFile_Parser import SycnParser
    new = SycnParser()
    new.parse("/CogWorks/cwl-data/Active_Projects/Tetris/External_Tournaments/CTWC19/meta-two/")


# testFunc()