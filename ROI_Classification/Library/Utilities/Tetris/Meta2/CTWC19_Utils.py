import pandas as pd
import numpy as np
from statistics import mean



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


"""
***This module is not tested and may not work***
Given the game and gaze data, align them in time by removing records from the higher frequency gaze 
data to downscale the entire data to the lower game frequency
Parameters:
  :param gameData:   A GameLog object containing the data to align
  :param gazeData:   A GazeLog object containing the data to align
  :param startTime:  The start time for the game in the Gaze Data (Unit: dame as the timestamp in the gaze data)
  :return:          A pandas dataframe with combined information information
"""
def alignData_GameGaze_downsample(gameData, gazeData, startTime):
    print("Aligning Data")

    if not valid_Game(gameData):
        print("Length of timestamps do not match other data in game data object so this file was ignored")
        return None
    if not valid_Gaze(gazeData):
        print("Length of timestamps do not match other data in gaze data object so this file was ignored")
        return None

    gameDuration = gameData.timeStamp[-1] - gameData.timeStamp[0]
    endTime = startTime + gameDuration

    # Find values closest to estimated start and end times of the game from the gaze data
    startTimeDifference = list(abs(np.array(gazeData.timeStamp) - startTime))
    startTimeIndex = np.where(startTimeDifference == np.amin(startTimeDifference))[0][0]
    endTimeDifference = list(abs(np.array(gazeData.timeStamp) - endTime))
    endTimeIndex = np.where(endTimeDifference == np.amin(endTimeDifference))[0][0]

    currGazeIndex = startTimeIndex
    currGameIndex = 0
    consolidatedDataList = [[gameData.timeStamp[currGameIndex], gazeData.timeStamp[currGazeIndex], gazeData.gazeX[currGazeIndex], \
                            gazeData.gazeY[currGazeIndex], gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], \
                            gazeData.eventID[currGazeIndex], gameData.boardRep[currGameIndex], gameData.zoidRep[currGameIndex]]]
    currGazeTimeDelta = 0
    nextRecordTime = 0
    # Performance stuff
    append = consolidatedDataList.append
    timeStamp_gaze = gazeData.timeStamp
    timeStamp_game = gameData.timeStamp
    # This loop is necessary because the frequency of recording game and gaze data are different, about ~4.5 gaze records per game record
    while(currGazeIndex < endTimeIndex and currGameIndex < len(timeStamp_game)-1):
        currGazeIndex += 1
        currGameIndex += 1

        prevGazeTimeDelta = 0
        currGazeTimeDelta += timeStamp_gaze[currGazeIndex] - timeStamp_gaze[currGazeIndex - 1]
        nextRecordTime += timeStamp_game[currGameIndex] - timeStamp_game[currGameIndex - 1]
        while(currGazeTimeDelta < nextRecordTime):
            currGazeIndex += 1
            prevGazeTimeDelta = currGazeTimeDelta
            currGazeTimeDelta += (timeStamp_gaze[currGazeIndex] - timeStamp_gaze[currGazeIndex - 1])
        
        # If previous gaze record was closer in time to current game record use that, corresponding to current game record
        if (abs(prevGazeTimeDelta - nextRecordTime) < abs(currGazeTimeDelta - nextRecordTime)):
            currGazeIndex -= 1

        append([timeStamp_game[currGameIndex], timeStamp_gaze[currGazeIndex], gazeData.gazeX[currGazeIndex], gazeData.gazeY[currGazeIndex], \
                gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], gazeData.eventID[currGazeIndex], gameData.boardRep[currGameIndex], \
                gameData.zoidRep[currGameIndex]])

    consolidatedDataDF = pd.DataFrame(consolidatedDataList, columns=["timeStamp", "eyeTracker_timeStamp", "gazeX", "gazeY", "gazeZ", "gazeClass", "gazeEventID", "boardRep", "zoidRep"])
    print("Alignment complete, total records: ", len(consolidatedDataList))
    return consolidatedDataDF


"""
Given the game and gaze data, align them in time by introducing redunduncies in the lower frequency game 
data to upscale the entire data to the higher gaze frequency
Parameters:
  :param gameData:   A GameLog object containing the data to align
  :param gazeData:   A GazeLog object containing the data to align
  :param startTime:  The start time for the game in the Gaze Data (Unit: dame as the timestamp in the gaze data)
  :return:          A pandas dataframe with combined information information
"""
def alignData_GameGaze_upsample(gameData, gazeData, startTime):
    print("Aligning Data")

    if not valid_Game(gameData):
        print("Length of timestamps do not match other data in game data object so this file was ignored")
        return None
    if not valid_Gaze(gazeData):
        print("Length of timestamps do not match other data in gaze data object so this file was ignored")
        return None

    gameDuration = gameData.timeStamp[-1] - gameData.timeStamp[0]
    endTime = startTime + gameDuration

    # Find values closest to estimated start and end times of the game from the gaze data
    startTimeDifference = list(abs(np.array(gazeData.timeStamp) - startTime))
    startTimeIndex = np.where(startTimeDifference == np.amin(startTimeDifference))[0][0]
    endTimeDifference = list(abs(np.array(gazeData.timeStamp) - endTime))
    endTimeIndex = np.where(endTimeDifference == np.amin(endTimeDifference))[0][0]

    currGazeIndex = startTimeIndex
    currGameIndex = 0
    consolidatedDataList = [[gameData.timeStamp[currGameIndex], gazeData.timeStamp[currGazeIndex], gazeData.gazeX[currGazeIndex], \
                            gazeData.gazeY[currGazeIndex], gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], \
                            gazeData.eventID[currGazeIndex], gameData.boardRep[currGameIndex], gameData.zoidRep[currGameIndex]]]
    currGazeIndex += 1
    nextGameFrameTime = 0
    cumulativeGazeTimeDelta = 0
    gazePerGame = [] # Get number of gaze frames per game frame
    # Performance stuff
    append = consolidatedDataList.append
    timeStamp_gaze = gazeData.timeStamp
    timeStamp_game = gameData.timeStamp
    appendCount = gazePerGame.append
    # This loop is necessary because the frequency of recording game and gaze data are different, about ~4.5 gaze records per game record
    # Outer loop, for looping throigh each game record
    while(currGazeIndex < endTimeIndex and currGameIndex < len(timeStamp_game)-1):
        count = 0
        currGameIndex += 1
        nextGameFrameTime += (timeStamp_game[currGameIndex] - timeStamp_game[currGameIndex - 1])

        # Multiple rows with same time but different information
        if (timeStamp_game[currGameIndex] - timeStamp_game[currGameIndex - 1]) == 0:
            append([timeStamp_game[currGameIndex], timeStamp_gaze[currGazeIndex], gazeData.gazeX[currGazeIndex], gazeData.gazeY[currGazeIndex], \
                    gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], gazeData.eventID[currGazeIndex], gameData.boardRep[currGameIndex], \
                    gameData.zoidRep[currGameIndex]])
            continue

        # cumulativeGazeTimeDelta += (timeStamp_gaze[currGazeIndex] - timeStamp_gaze[currGazeIndex - 1])

        # Inner loop, for looping through multiple gaze records for each game record
        while(cumulativeGazeTimeDelta < nextGameFrameTime):
            count += 1
            cumulativeGazeTimeDelta += (timeStamp_gaze[currGazeIndex] - timeStamp_gaze[currGazeIndex - 1])
            append([timeStamp_game[currGameIndex], timeStamp_gaze[currGazeIndex], gazeData.gazeX[currGazeIndex], gazeData.gazeY[currGazeIndex], \
                    gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], gazeData.eventID[currGazeIndex], gameData.boardRep[currGameIndex], \
                    gameData.zoidRep[currGameIndex]])
            currGazeIndex += 1
        
        appendCount(count)
        
    consolidatedDataDF = pd.DataFrame(consolidatedDataList, columns=["timeStamp", "eyeTracker_timeStamp", "gazeX", "gazeY", "gazeZ", "gazeClass", "gazeEventID", "boardRep", "zoidRep"])
    print("Alignment complete, total records: ", len(consolidatedDataDF))
    print("Number of gaze frames per game frame: ", mean(gazePerGame))
    return consolidatedDataDF