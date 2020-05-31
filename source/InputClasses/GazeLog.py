class GazeLog:
    def __init__(self, gazeDF):
        self.subjectID = ""    #e.g. 19CTWC007
        self.sessionID = 0    #Identifier for which gaze recording in the study this is (usually unneeded for popstudy)
        self.timeStamp = []   #list of timestamps
        self.gazeX = []       #time series of X gaze coords
        self.gazeY = []       #time series of Y gaze coords
        self.gazeZ = []       #time series of Z gaze coords
        parseDF(gazeDF)
    pass