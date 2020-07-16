# Libraries
from sqlalchemy import create_engine
import pymysql

import pandas as pd
import numpy as np
from ...DataClasses.GameLog import GameLog




class GameParser:
        def __init__(self):
                # Create connection with database
                sqlEngine = create_engine('mysql+pymysql://tetris_ro:CogWorksTetris@cwl-sql.hass.rpi.edu/TetrisMetaTWO', pool_recycle=3600)
                self.dbConnection = sqlEngine.connect()


        def parse(self, gameID, colNames):
                print("Getting game metadata.")
                metaData_Query = "SELECT * FROM GameSummaries WHERE gameID = " + str(gameID)
                metaData_DF = pd.read_sql(metaData_Query, self.dbConnection)
                print("Got game metadata.")

                print("Getting game data.")
                gameData_Query = "SELECT ts, system_ticks, board_rep, zoid_rep\
                        FROM GameLogs WHERE gameID = " + str(gameID)
                game_DF = pd.read_sql(gameData_Query, self.dbConnection)
                print("Got game data.")

                gameData = GameLog()
                gameData.subjectID = metaData_DF[colNames[0]].iloc[0]
                gameData.sessionNum = metaData_DF[colNames[1]].iloc[0]
                gameData.gameNum = metaData_DF[colNames[2]].iloc[0]
                gameData.resolution = metaData_DF[colNames[3]].iloc[0]
                # Convert timestamp to milliseconds
                gameData.timeStamp = list(np.ceil(np.array(game_DF[colNames[4]].tolist()) * 1000))
                gameData.System_timeStamp = game_DF[colNames[5]].tolist()
                gameData.boardRep = game_DF[colNames[6]].tolist()
                gameData.zoidRep = game_DF[colNames[7]].tolist()

                return gameData


        def get_gameID_fromInformation(self, Event_Identifier, subID, gameNum, sessNum):
                print("This function does not work")
                return None
                gameID_Query = "SELECT gameID FROM GameSummaries WHERE ... = " + str(gameID)
                metaData_DF = pd.read_sql(gameID_Query, self.dbConnection)
                print(type(metaData_DF))
                # if #Check if gameID for provided details exist, if not return None:

                # else:
                #         print("No data for subject: ", subjectID, ", Game: ", gameNum, ", Session: ", sessionNum)
                #         return None


        """
        Parameters:
        :param syncfile_path: The path where the sync file exsts, the data from game files in that directory will be returned
        :param gameID_columnName: The name of the column containing gameID in the database 
        :param root_dir: The root directory containing all game files relevant to current analysis. Ex: CTWC19
        """
        def get_gameID_fromFilePath(self, syncfile_path, gameID_columnName, root_dir):
                # Begin the path from the Tetris directory and en at experiment directory
                experiment_path = syncfile_path.split('/')[-1]
                # experiment_path = '/'.join(experiment_path[experiment_path.index(root_dir):-1])
                # Find all entries that have the path as substring
                experiment_path = '%%'+experiment_path+'%%'
                gameID_Query = "SELECT " + gameID_columnName + " FROM GameSummaries WHERE filePath LIKE '" + str(experiment_path) + "'"
                gameID_DF = pd.read_sql(gameID_Query, self.dbConnection)
                if gameID_DF.shape[0] == 0:
                        print("There were no entries corresponding to: \n", experiment_path)
                        return None
                else:
                        print("Got game IDs")
                        return gameID_DF[gameID_columnName].tolist()


        def get_DBconnection(self):
                return self.dbConnection