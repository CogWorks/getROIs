class GazeLog:
    def __init__(self):
        self.__subjectID = ""       # e.g. 19CTWC007
        self.__date = 0             # Identifier for which gaze recording in the study this is (usually unneeded for popstudy)
        self.__startTime = 0        # Identifier for which game in the study this is
        self.__timeStamp = []       # list of timestamps
        self.__gazeX = []           # time series of X gaze coords
        self.__gazeY = []           # time series of Y gaze coords
        self.__gazeZ = []           # time series of Z gaze coords
        self.__gazeClass = []       # saccade/fixation/...
        self.__eventID = []         # The event identifier for how many times gaze class changed
        

    def get_subjectID(self):
        return self.__subjectID

    def set_subjectID(self, subjectID):
        self.__subjectID = subjectID

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_startTime(self):
        return self.__startTime

    def set_startTime(self, startTime):
        self.__startTime = startTime

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

    def get_gazeClass(self):
        return self.__gazeClass

    def set_gazeClass(self, gazeClass):
        self.__gazeClass = gazeClass

    def get_eventID(self):
        return self.__eventID

    def set_eventID(self, eventID):
        self.__eventID = eventID