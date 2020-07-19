# Parameters:
gazeData_fileType = ".tsv"
# Parameters:
#   sourcePath: Directory containing all the source files [should be a flat directory]
#   syncFile: If this is set to True it will look for sync files for the games 
#               sync files contain Recording time stamps and their corrsponding system timestamps,
#               in the CTWC19 Data.
gazeData_delimeter = "\t"
gazeData_colNames = ["Participant name", "Recording date", "Recording start time", "timestamp", "x", "y", "Eye position left Z (DACSmm)", "class"]
gameData_colNames = ["SID", "SessionNum", "GameNum", "Screen_Resolution", "ts", "system_ticks", "board_rep", "zoid_rep"]
Event_Identifier = "CTWC19"
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
import pandas as pd
import numpy as np

from Library.Parsers.GazeParsers.Tobii_gazeTools_CSV_Parser import GazeParser
from Library.Parsers.GameParsers.Meta2_SQL_Parser import GameParser
from Library.Parsers.OtherParsers.CTWC19_SyncFile_Parser import SycnParser
from Library.Tetris.Utilities.CTWC19_Utils import alignData_GameGaze as align
from Library.ROI_Codes.GenerateROI import GetROI_Meta2
GetROI_Obj = GetROI_Meta2()


def getClassifications():
    count = 0
    gazeParser = GazeParser()
    gameParser = GameParser()
    # syncParser = SycnParser("/CogWorks/cwl-data/Active_Projects/Tetris/External_Tournaments/CTWC19/meta-two/")

    syncFile = pd.read_csv('/CogWorks/cwl-data/Active_Projects/Tetris/External_Tournaments/CTWC19/Tobii-LabPro/CTWC19 Sync-Times.tsv', sep = '\t')
    syncFile.replace(np.NaN, ' ', regex=False, inplace=True)
    syncFile = syncFile[syncFile['Gaze Data Start Time'] != ' ']
    # Convert to datetime
    syncFile['Gaze Data Start Time'] = syncFile['Gaze Data Start Time'].astype(str) + '000' # Convert to microsecond to match format
    syncFile['Gaze Data Start Time'] = pd.to_datetime(syncFile['Gaze Data Start Time'], format= '%H:%M:%S.%f').dt.time
    
    
    # Loop through all gaze files in the directory
    for inFile in os.scandir(sourcePath):
        if (inFile.is_file() and inFile.path.endswith(gazeData_fileType)):
            print("Processing data corresponding to gaze file:\n", inFile.path.split("/")[-1].strip())
            count += 1

            # Parse the gaze file and get gaze object with all information
            gazeData = gazeParser.parse(inFile.path, gazeData_fileType, gazeData_delimeter, gazeData_colNames)
            if gazeData == None:
                continue

            # Get file paths of all experiments corresponding to the gaze file (generally 1)
            # experimentFile_paths = syncParser.get_filePath_from_eyetrackerTime(gazeData.timeStamp, gazeData.subjectID)
            # if experimentFile_paths == None:
            #     continue
            # elif len(experimentFile_paths)>1:
            #     print("Has more than one associated expeiment:\n", experimentFile_paths)

            currSyncInfo = syncFile[(syncFile.GazeFile ==  inFile.path.split(' ')[1]) & (syncFile.GameFile.str.contains(inFile.path.split(' ')[2])) & (syncFile.GazeFile != 'Bad Data')]
            if currSyncInfo.shape[0] == 0:
                # If no ecords exist skip file
                print("The game either contains bad gaze-data or does not have associated gaze files")
                continue
            
            # Loop through each experiment
            for _, currGame in currSyncInfo.iterrows():
                gameFile = currGame.GameFile
                startTime = currGame['Gaze Data Start Time']
                startTime_millisecond = ((((startTime.hour * 60) + startTime.minute) * 60 + startTime.second) * 1000) + (startTime.microsecond / 1000)
                print("Processing data for game file:\n", gameFile.strip())
                # print(gameFile, startTime)
                # Get ID for the game
                gameID = gameParser.get_gameID_fromFilePath(gameFile, 'gameID', 'CTWC19')
                if gameID == None:
                    continue
                # Fetch the game data
                gameData = gameParser.parse(gameID[0], gameData_colNames)
                if gameData == None:
                    continue
                combinedDF = align(gameData, gazeData, startTime_millisecond)
                dynamicObjectColumns = ["gazeX", "gazeY", "gazeZ", "gazeClass"]
                gazeInformationColumns = ["boardRep", "zoidRep"]
                ROI_DF = GetROI_Obj.generateROIClassification(combinedDF, dynamicObjectColumns, gazeInformationColumns, syncDelayTolerance=0)
            print("Processing ", count, " files complete...")







getClassifications()
