# Contains code for parsing sync files generated for CTWC19 data
# These files contain Recording timestamp and corresponding System timestamp
# These files are meant to be used to align game and gaze data

import os
import pandas as pd
from ...DataClasses.SyncLog import SyncLog

class SycnParser:
    def __init__(self, base_dir):
        self.syncFiles = {}        #Dictionary; Key: file path; value: data for all sync files from CTWC19
        self.parse(base_dir)


    def parse(self, base_dir):
        for subdir, dirs, files in os.walk(base_dir):
            if not "Logs" in subdir:                    #Ignore all directories which are not game logs
                continue
            for file in files:
                if file.endswith("tobii-sync.tsv"):     #Look for Sync files
                    if not "test" in file.lower():      #Ignore irrelevant data from test cases
                        # print(os.path.join(subdir, file))
                        filePath = os.path.join(subdir, file)
                        syncDF = pd.read_csv(filePath, sep='\t')
                        syncLog = SyncLog()
                        syncLog.system_clock = syncDF["system_clock"].tolist()
                        syncLog.eyetracker_clock = syncDF["spectrum_clock"].tolist()
                        self.syncFiles[filePath] = syncLog
        print("Sync-file Parsing Complete.")


    def get_filePath_from_eyetrackerTime(self, timestamp):
        filePath = []
        for path, syncFile in self.syncFiles.items():
            # Checks for any common values between two lists
            if len(set(syncFile.eyetracker_clock) & set(timestamp)) > 0:
                filePath.append(path)
        return filePath


    def get_filePath_from_systemTime(self, timestamp):
        pass


    def get_data_from_path(self, path):
        pass
