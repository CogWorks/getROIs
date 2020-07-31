# Parameters:
#   sourcePath: Directory containing all the source files [should be a flat directory]
gazeData_delimeter = "\t"
gazeData_colNames = ["Participant name", "Recording date", "Recording start time", "timestamp", "x", "y", "Eye position left Z (DACSmm)", "class", "event_ids"]
gameData_colNames = ["SID", "SessionNum", "GameNum", "Screen_Resolution", "ts", "system_ticks", "board_rep", "zoid_rep"]
# dynamicObjectColumns = ["boardRep", "zoidRep"]
# gazeInformationColumns = ["gazeX", "gazeY", "gazeZ", "gazeClass"]
Event_Identifier = "CTWC19"
sourcePath = "/CogWorks/cwl-data/Active_Projects/Tetris/Workspaces/Banerjee/Gaze_Stuff/R_Files/Gaze_Outputs/CTWC19/"
gazeData_fileType = ".tsv"
outputLocation = "/CogWorks/cwl-data/Active_Projects/Tetris/Workspaces/Banerjee/Gaze_Stuff/ROI_Outputs/"

# Import Libraries
import os
import pandas as pd
import numpy as np

from Library.Parsers.GazeParsers.Tobii_gazeTools_CSV_Parser import GazeParser
from Library.Parsers.Tetris.Meta2.Meta2_SQL_Parser import GameParser
from Library.Utilities.Tetris.Meta2.CTWC19_Utils import alignData_GameGaze_upsample as align
from Library.ROI_Codes.GenerateROI_Meta2 import GetROI_Meta2
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

            currSyncInfo = syncFile[(syncFile.GazeFile == inFile.path.split("/")[-1].strip().split()[1]) & \
                                    (syncFile.GameFile.str.contains(inFile.path.split("/")[-1].strip().split()[2])) & \
                                    (syncFile.Comments != 'Bad Data') & (syncFile.Comments != 'No Gaze Data') & (syncFile.Comments != 'Test Data')]


            if currSyncInfo.shape[0] == 0:
                # If no ecords exist skip file
                print("The game contains bad gaze-data or is test data")
                continue
            
            # Loop through each experiment
            for _, currGame in currSyncInfo.iterrows():
                gameFile = currGame.GameFile
                print("Processing data for game file:\n", gameFile.strip())

                startTime = currGame['Gaze Data Start Time']
                startTime_millisecond = ((((startTime.hour * 60) + startTime.minute) * 60 + startTime.second) * 1000) + (startTime.microsecond / 1000)

                # # Debugging stuff
                # if not gameFile.strip() == "19CTWC015_2019-10-20_04-25-29_nonxbo_shortstart.env_ninetillend.tsv":
                #     continue

                # Get ID for the game
                gameID = gameParser.get_gameID_fromFilePath(gameFile, 'gameID', 'CTWC19')
                if gameID == None:
                    continue

                # Fetch the game data
                gameData = gameParser.parse(gameID[0], gameData_colNames)
                if gameData == None:
                    continue

                # Align the Game with the Gaze file
                combinedDF = align(gameData, gazeData, startTime_millisecond)
                combinedDF.to_csv(outputLocation + "Aligned_" + gameFile.strip(), sep = '\t')

                # Get ROI Classification
                ROI_DF = GetROI_Obj.generateROIClassification(combinedDF, syncDelayTolerance=0)
                ROI_DF.to_csv(outputLocation + "ROI_" + gameFile.strip(), sep = '\t')
                print("Processing current game file complete...")

            print("Processing ", count, " gaze files complete...")
            print("----------------------------------X---------------------------------------")







getClassifications()
