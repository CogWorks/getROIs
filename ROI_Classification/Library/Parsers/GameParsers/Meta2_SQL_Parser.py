# Libraries
from sqlalchemy import create_engine
import pymysql

from ...DataClasses.GameLog import GameLog
import pandas as pd



class GameParser:
        def __init__(self):
                # Create connection with database
                sqlEngine = create_engine('mysql+pymysql://tetris_ro:CogWorksTetris@cwl-sql.hass.rpi.edu/TetrisMetaTWO', pool_recycle=3600)
                self.dbConnection = sqlEngine.connect()


        def parse(self, gameID, colNames):
                metaData_Query = "SELECT * FROM GameSummaries WHERE gameID = " + str(gameID)
                metaData_DF = pd.read_sql(metaData_Query, self.dbConnection)
                print("Got game metadata.")
                # print(metaData_DF.columns)

                gameData_Query = "SELECT ts, system_ticks, board_rep, zoid_rep\
                        FROM GameLogs WHERE gameID = " + str(gameID)
                game_DF = pd.read_sql(gameData_Query, self.dbConnection)
                print("Got game data.")
                # print(game_DF.columns)

                gameData = GameLog()
                gameData.subjectID = metaData_DF[colNames[0]][0]
                print(gameData.subjectID)
                gameData.sessionNum = metaData_DF[colNames[1]][0]
                gameData.gameNum = metaData_DF[colNames[2]][0]
                gameData.resolution = metaData_DF[colNames[3]][0]
                gameData.timeStamp = game_DF[colNames[4]]
                gameData.System_timeStamp = game_DF[colNames[5]]
                gameData.boardRep = game_DF[colNames[6]]
                gameData.zoidRep = game_DF[colNames[7]]

                return gameData


        def get_gameID(self):
                pass
                gameID_Query = "SELECT gameID FROM GameSummaries WHERE gameID = " + str(gameID)
                metaData_DF = pd.read_sql(gameID_Query, self.dbConnection)
                print(type(metaData_DF))
                # if #Check if gameID for provided details exist, if not continue to next file:

                # else:
                #         print("No data for subject: ", subjectID, ", Game: ", gameNum, ", Session: ", sessionNum)
                #         return None


        def get_DBconnection(self):
                return self.dbConnection