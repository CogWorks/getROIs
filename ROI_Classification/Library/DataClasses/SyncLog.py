class SyncLog:
    def __init__(self):
        self.__system_clock = []      #time series of system (local) clock ticks
        self.__eyetracker_clock =[]   #time series of eyetracker (remote) clock ticks
        

    def get_system_clock(self):
        return self.__system_clock

    def set_system_clock(self, system_clock):
        self.__system_clock = system_clock

    def get_eyetracker_clock(self):
        return self.__eyetracker_clock

    def set_eyetracker_clock(self, eyetracker_clock):
        self.__eyetracker_clock = eyetracker_clock
        

 