# The call to this class takes as input, a pandas dataframe containing the following columns:
# Name          Type                    Description
# ------------------------------------------------------------------------------------
# subjectID     String      
# sessionID     Numeric                 Identifier for which game in the study this is
# timeStamp     List<numeric>           List of timestamps
# boardRep      List<List<List>>        Time series of board representations
# zoidRep       List<List<List>>        Time series of falling zoid representations


class GameLog:
    def __init__(self, gameDF):
        self.subjectID = ""  #e.g. 19CTWC007
        self.sessionID = 0   #Identifier for which game in the study this is
        self.timeStamp = []  #list of timestamps
        self.boardRep  = []  #time series of board representations
        self.zoidRep   = []  #time series of falling zoid representations
        
        readDF(gameDF)

    pass