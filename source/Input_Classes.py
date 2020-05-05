class GameLog:
    def __init__(self):
        self.subjectID = 0  #e.g. 19CTWC007
        self.sessionID = 0   #Identifier for which game in the study this is
        self.timeStamp = []  #list of timestamps
        self.boardRep  = []  #time series of board representations
        self.zoidRep   = []  #time series of falling zoid representations


class GazeLog:
    def __init__(gazeDF):
        subjectID       #e.g. 19CTWC007
        sessionID       #Identifier for which gaze recording in the study this is (usually unneeded for popstudy)
        timeStamp       #list of timestamps
        gazeX           #time series of X gaze coords
        gazeY           #time series of Y gaze coords
        gazeZ           #time series of Z gaze coords

    pass

class SyncLog:
    def __init__(syncDF):
        system_clock    #time series of system (local) clock ticks
        spectrum_clock  #time series of eyetracker (remote) clock ticks
        

 