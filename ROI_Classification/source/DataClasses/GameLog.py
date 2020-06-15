# The call to this class takes as input, a pandas dataframe containing the following columns:
# Name          Type                    Description
# ------------------------------------------------------------------------------------
# subjectID     String      
# sessionID     Numeric                 Identifier for which game in the study this is
# timeStamp     List<numeric>           List of timestamps
# boardRep      List<List<List>>        Time series of board representations
# zoidRep       List<List<List>>        Time series of falling zoid representations


class GameLog:
    def __init__(self, gameData, metaData):
        self.subjectID = ""             #e.g. 19CTWC007
        self.sessionID = 0              #Identifier for which game in the study this is
        self.gameID = 0                 #Identifier for which game in the study this is
        self.resolution = []            #Identifier for which game in the study this is
        self.timeStamp = []             #List of timestamps
        self.System_timeStamp = []      #List of system timestamps
        self.boardRep = []              #Time series of board representations
        self.zoidRep = []               #Time series of falling zoid representations
        setData(gameData, metaData)


    def setData(self, gameData, metaData):
        self.subjectID = metaData[]
        self.sessionID = metaData[]
        self.gameID = metaData[]
        self.resolution = metaData[]
        self.timeStamp = gameData[]
        self.System_timeStamp = gameData[]
        self.boardRep = gameData[]
        self.zoidRep = gameData[]


    def getData():
        return(self.subjectID, self.sessionID, self.gameID, self.resolution, self.timeStamp, self.System_timeStamp, self.boardRep, self.zoidRep)