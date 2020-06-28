import pandas as pd



def valid_Game(data):
    if len(data.timeStamp) == len(data.System_timeStamp):
        if len(data.timeStamp) == len(data.boardRep):
            if len(data.timeStamp) == len(data.zoidRep):
                return True
    return False

def valid_Gaze(data):
    if len(data.timeStamp) == len(data.gazeX):
        if len(data.timeStamp) == len(data.gazeY):
            if len(data.timeStamp) == len(data.gazeZ):
                if len(data.timeStamp) == len(data.gazeClass):
                    return True
    return False

def valid_Sync(data):
    if len(data.system_clock) == len(data.eyetracker_clock):
        return True
    return False


# Given a the game data 
# Parameters:
#   gameData: A GameLog object containing the data to align
#   syncData: A SyncLog object containing the data to align
#   gazeData: A GazeLog object containing the data to align
# Returns: A pandas dataframe with combined information information
def alignData_GameGaze(gameData, syncData, gazeData):
    if not valid_Game(gameData):
        print("Length of timestamps do not match other data in game data object so this file was ignored")
        return None
    if not valid_Gaze(gazeData):
        print("Length of timestamps do not match other data in gaze data object so this file was ignored")
        return None
    if not valid_Sync(syncData):
        print("Length of system and eyetrcker clock do not match in sync data object so this file was ignored")
        return None
    
    dataDF = pd.DataFrame()
    
    return dataDF