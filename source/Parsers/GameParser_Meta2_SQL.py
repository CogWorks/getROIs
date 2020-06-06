# Parameters
gameList_Query = "SELECT gameID FROM GameSummaries WHERE filePath LIKE '%CTWC19%' AND ECID <> '9test' OR ECID <> 'ultraspeedtetris'"


# Libraries
from sqlalchemy import create_engine
import pymysql
import pandas as pd




gameList_df = pd.read_sql(gameList_Query, dbConnection)
gameIDs = gameList_df['gameID']

for id in gameIDs:
        pass

# query = "SELECT * FROM GameSummaries WHERE gameID = 5"
# df = pd.read_sql(query, dbConnection)

# query = "SELECT * FROM GameLogs WHERE gameID = ?"
# df = pd.read_sql(query, dbConnection, params=(10))


def parse(gameID):

        # Create connection with database
        sqlEngine = create_engine('mysql+pymysql://tetris_ro:CogWorksTetris@cwlsql.hass.rpi.edu/TetrisMetaTWO', pool_recycle=3600)
        dbConnection = sqlEngine.connect()

        query = "SELECT GameSummaries.gameID, SID, USID, SessionNum, GameNum, Window_Height, Window_Width, ts, system_ticks, board_rep, zoid_rep\
                FROM GameSummaries INNER JOIN GameLogs ON GameSummaries.gameID = GameLogs.gameID\
                WHERE GameSummaries.gameID IN"
        resultDF = pd.read_sql(query, dbConnection)