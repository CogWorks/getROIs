class GazeLog:
    def __init__(self):
        self.__subjectID = ""       #e.g. 19CTWC007
        self.__sessionNum = 0       #Identifier for which gaze recording in the study this is (usually unneeded for popstudy)
        self.__gameNum = 0          #Identifier for which game in the study this is
        self.__timeStamp = []       #list of timestamps
        self.__gazeX = []           #time series of X gaze coords
        self.__gazeY = []           #time series of Y gaze coords
        self.__gazeZ = []           #time series of Z gaze coords
        

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

    def get_timeStamp(self):
        return self.__timeStamp

    def set_timeStamp(self, timeStamp):
        self.__timeStamp = timeStamp

    def get_gazeX(self):
        return self.__gazeX

    def set_gazeX(self, gazeX):
        self.__gazeX = gazeX

    def get_gazeY(self):
        return self.__gazeY

    def set_gazeY(self, gazeY):
        self.__gazeY = gazeY

    def get_gazeZ(self):
        return self.__gazeZ

    def set_gazeZ(self, gazeZ):
        self.__gazeZ = gazeZ