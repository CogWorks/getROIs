# Contains code for parsing sync files generated for CTWC19 data
# These files contain Recording timestamp and corresponding System timestamp
# These files are meant to be used to align game and gaze data

import os
import pandas as pd
from ...Tetris.DataClasses.SyncLog import SyncLog

class SycnParser:
    def __init__(self, base_dir):
        self.syncFiles = {}        #Dictionary; Key: file path; value: data for all sync files from CTWC19
        self.parse(base_dir)


    def parse(self, base_dir):
        for subdir, dirs, files in os.walk(base_dir):
            if not "Logs" in subdir:                    #Ignore all directories which are not game logs
                continue
            for syncFile in files:
                if syncFile.endswith("tobii-sync.tsv"):     #Look for Sync files
                    if not "test" in syncFile.lower():      #Ignore irrelevant data from test cases
                        filePath = os.path.join(subdir, syncFile)
                        syncDF = pd.read_csv(filePath, sep='\t')
                        syncLog = SyncLog()
                        syncLog.subjectID = syncFile.split("_")[1]
                        syncLog.system_clock = syncDF["system_clock"].tolist()
                        syncLog.eyetracker_clock = syncDF["spectrum_clock"].tolist()
                        self.syncFiles[filePath] = syncLog
        print("Sync-file Parsing Complete.")


    # Parameters:
    #   timestamp: It takes the timestamps column from the gaze file as list and compares it against all sync files
    #               to determine which sync file corresponds to the gaze data
    #   subjectID: This is necessary because, the multiple eye-trackers have the same timestamp.
    #              So, a combination of timestamp and subject ID forms a unique key for each game.
    def get_filePath_from_eyetrackerTime(self, timestamp, subjectID):
        filePath = []
        for path, syncFile in self.syncFiles.items():
            if syncFile.subjectID == subjectID:
                # Checks for common values between two lists
                if len(set(syncFile.eyetracker_clock) & set(timestamp)) > 0:
                    filePath.append(path)
        if len(filePath) == 0:
            print("No sync files were found for the data")
            return None
        else:
            print("Got sync file")
            return filePath


    # Parameters:
    #   timestamp: It takes the timestamps column from the game file as list and compares it against all sync files
    #               to determine which sync file corresponds to the game data
    #   subjectID: This is necessary because, the multiple computers have the same timestamp.
    #              So, a combination of timestamp and subject ID forms a unique key for each game.
    def get_filePath_from_systemTime(self, timestamp, subjectID):
        pass


    def get_data_from_path(self, path):
        return self.syncFiles[path]
