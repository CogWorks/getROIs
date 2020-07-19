import pandas as pd
import numpy as np



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
Given the game and gaze data align them in time
Parameters:
  :param gameData:   A GameLog object containing the data to align
  :param gazeData:   A GazeLog object containing the data to align
  :param startTime:  The start time for the game in the Gaze Data (Unit: dame as the timestamp in the gaze data)
  :return:          A pandas dataframe with combined information information
"""
def alignData_GameGaze(gameData, gazeData, startTime):
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

    consolidatedDataList = [[gameData.timeStamp[currGameIndex], gazeData.gazeX[currGazeIndex], gazeData.gazeY[currGazeIndex], \
                            gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], gameData.boardRep[currGameIndex], \
                            gameData.zoidRep[currGameIndex]]]
    # This loop is necessary because the frequency of recording game and gaze data are different, about ~4.5 gaze records per game record
    while(currGazeIndex < endTimeIndex and currGameIndex < len(gameData.timeStamp)-1):
        currGazeIndex += 1
        currGameIndex += 1

        prevGazeTimeDelta = 0
        currGazeTimeDelta = gazeData.timeStamp[currGazeIndex] - gazeData.timeStamp[currGazeIndex - 1]
        nextRecordTime = gameData.timeStamp[currGameIndex] - gameData.timeStamp[currGameIndex - 1]
        while(currGazeTimeDelta < nextRecordTime):
            currGazeIndex += 1
            prevGazeTimeDelta = currGazeTimeDelta
            currGazeTimeDelta += (gazeData.timeStamp[currGazeIndex] - gazeData.timeStamp[currGazeIndex - 1])
        
        # If previous gaze record was closer in time to current game record use that, corresponding to current game record
        if (abs(prevGazeTimeDelta - nextRecordTime) < abs(currGazeTimeDelta - nextRecordTime)):
            currGazeIndex -= 1

        consolidatedDataList.append([gameData.timeStamp[currGameIndex], gazeData.gazeX[currGazeIndex], gazeData.gazeY[currGazeIndex], \
                                    gazeData.gazeZ[currGazeIndex], gazeData.gazeClass[currGazeIndex], gameData.boardRep[currGameIndex], \
                                    gameData.zoidRep[currGameIndex]])

    consolidatedDataDF = pd.DataFrame(consolidatedDataList, columns=["timeStamp", "gazeX", "gazeY", "gazeZ", "gazeClass", "boardRep", "zoidRep"])
    print("Alignment complete")
    return consolidatedDataDF