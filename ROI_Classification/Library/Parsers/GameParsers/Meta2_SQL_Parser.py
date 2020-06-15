# Libraries
from sqlalchemy import create_engine
import pymysql
import pandas as pd

from ....DataClasses.GameLog import GameLog


def parse(subjectID, gameNum, sessionNum):

        if #check if connection works
                # Create connection with database
                sqlEngine = create_engine('mysql+pymysql://tetris_ro:CogWorksTetris@cwlsql.hass.rpi.edu/TetrisMetaTWO', pool_recycle=3600)
                dbConnection = sqlEngine.connect()
        else:
                # raise exception and close program with error
                pass

        if #Check if gameID for provided details exist, if not continue to next file
        else:
                print("No data for subject: ", subjectID, ", Game: ", gameNum, ", Session: ", sessionNum)
                return None

        metaData_Query = "SELECT gameID, SID, USID, SessionNum, GameNum, Window_Height, Window_Width\
                FROM GameSummaries WHERE gameID = " + gameID
        metaData_DF = pd.read_sql(metaData_Query, dbConnection)

        gameData_Query = "SELECT ts, system_ticks, board_rep, zoid_rep\
                FROM GameLogs WHERE gameID = " + gameID
        game_DF = pd.read_sql(gameData_Query, dbConnection)\

        gameData = GameLog()
        gameData.subjectID = metaData_DF[]
        gameData.sessionNum = metaData_DF[]
        gameData.gameNum = metaData_DF[]
        gameData.resolution = metaData_DF[]
        gameData.timeStamp = game_DF[]
        gameData.System_timeStamp = game_DF[]
        gameData.boardRep = game_DF[]
        gameData.zoidRep = game_DF[]

        return gameData