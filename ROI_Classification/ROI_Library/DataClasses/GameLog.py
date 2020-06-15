# The call to this class takes as input, a pandas dataframe containing the following columns:
# Name          Type                    Description
# ------------------------------------------------------------------------------------
# subjectID     String      
# sessionNum     Numeric                 Identifier for which game in the study this is
# timeStamp     List<numeric>           List of timestamps
# boardRep      List<List<List>>        Time series of board representations
# zoidRep       List<List<List>>        Time series of falling zoid representations


class GameLog:
    def __init__(self):
        self.__subjectID = ""             #e.g. 19CTWC007
        self.__sessionNum = 0              #Identifier for which game in the study this is
        self.__gameNum = 0                 #Identifier for which game in the study this is
        self.__resolution = []            #Identifier for which game in the study this is
        self.__timeStamp = []             #List of timestamps
        self.__System_timeStamp = []      #List of system timestamps
        self.__boardRep = []              #Time series of board representations
        self.__zoidRep = []               #Time series of falling zoid representations
        

    def get_subjectID(self):
        return self.__subjectID

    def set_subjectID(self, subjectID):
        self.__subjectID = subjectID

    def get_sessionNum(self):
        return self.__sessionNum

    def set_sessionNum(self, sessionNum):
        self.__sessionNum = sessionNum

    def get_gameNum(self):
        return self.__gameNum

    def set_gameNum(self, gameNum):
        self.__gameNum = gameNum

    def get_resolution(self):
        return self.__resolution

    def set_resolution(self, resolution):
        self.__resolution = resolution

    def get_timeStamp(self):
        return self.__timeStamp

    def set_timeStamp(self, timeStamp):
        self.__timeStamp = timeStamp

    def get_System_timeStamp(self):
        return self.__System_timeStamp

    def set_System_timeStamp(self, System_timeStamp):
        self.__System_timeStamp = System_timeStamp

    def get_boardRep(self):
        return self.__boardRep

    def set_boardRep(self, boardRep):
        self.__boardRep = boardRep

    def get_zoidRep(self):
        return self.__zoidRep

    def set_zoidRep(self, zoidRep):
        self.__zoidRep = zoidRep