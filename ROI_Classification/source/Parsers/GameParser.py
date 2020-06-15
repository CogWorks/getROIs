# Libraries
from sqlalchemy import create_engine
import pymysql
import pandas as pd

from ..DataClasses.GameLog import GameLog


class Meta2_SQL:
        def __init__(self):
                pass

        def parse(self, gameID):

                # Create connection with database
                sqlEngine = create_engine('mysql+pymysql://tetris_ro:CogWorksTetris@cwlsql.hass.rpi.edu/TetrisMetaTWO', pool_recycle=3600)
                dbConnection = sqlEngine.connect()

                metaData_Query = "SELECT gameID, SID, USID, SessionNum, GameNum, Window_Height, Window_Width\
                        FROM GameSummaries WHERE gameID = " + gameID
                metaData_DF = pd.read_sql(gameData_Query, dbConnection)

                gameData_Query = "SELECT ts, system_ticks, board_rep, zoid_rep\
                        FROM GameLogs WHERE gameID = " + gameID
                gameData_DF = pd.read_sql(metaData_Query, dbConnection)

                GameLog(gameData_DF, metaData_DF)