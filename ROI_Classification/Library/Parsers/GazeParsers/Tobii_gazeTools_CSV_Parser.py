import os
import pandas as pd

from ...Tetris.DataClasses.GazeLog import GazeLog

class GazeParser:
    def __init__(self):
        pass

    """
    This is a parser function that can parse 'seperated value' files (Ex: csv, tsv)
    Parameters:
      :param gazeFile: String for the absolute path to the file
      :param fileExtension: String value for the type of files to read (Ex: '.tsv', '.csv') 
      :param delimeter: string for the character separating the values (Ex: '\t' for tab-separated values)
      :param colNames: Names of columns (list) in the file, corresponding to the data [should maintain order]
      :return: a GazeLog Object
    """
    def parse(self, gazeFile, fileExtension, delimeter, colNames):
        if (gazeFile.endswith(fileExtension)):
            gazeDF = pd.read_csv(gazeFile, sep=delimeter)

            # Find and delete rows with timestamp = 0, these donot have any data
            noData_indices = gazeDF[gazeDF[colNames[3]] == 0 ].index
            gazeDF.drop(noData_indices , inplace=True)
            
            gazeData = GazeLog()
            gazeData.subjectID = gazeDF[colNames[0]].iloc[0]
            gazeData.date = gazeDF[colNames[2]].iloc[0]
            gazeData.startTime = gazeDF[colNames[2]].iloc[0]
            gazeData.timeStamp = gazeDF[colNames[3]].tolist()
            gazeData.gazeX = gazeDF[colNames[4]].tolist()
            gazeData.gazeY = gazeDF[colNames[5]].tolist()
            gazeData.gazeZ = gazeDF[colNames[6]].tolist()
            gazeData.gazeClass = gazeDF[colNames[7]].str.lower().tolist()
            gazeData.eventID = gazeDF[colNames[8]].tolist()

            # # Split data into periods of fixations
            # from itertools import groupby
            # tempList1 = gazeData.gazeClass[20212 : 75113]
            # tempList2 = gazeData.eventID[20212 : 75113]
            # curr_Index = 0
            # fixationPeriods = []
            # append = fixationPeriods.append
            # for currPeriod, periodChunk in groupby(tempList1):
            #     periodChunk_len = len(list(periodChunk))
            #     if currPeriod.lower() == 'fixation':
            #         # Divide each fixation chunk into multiple events (each for a different fixation), if exists
            #         subEvents = tempList2[curr_Index : (curr_Index + (periodChunk_len - 1))]
            #         for currSubperiod, subperiodChunk in groupby(subEvents):
            #             subperiodChunk_len = len(list(subperiodChunk))
            #             if subperiodChunk_len > 2:
            #                 append((curr_Index, (curr_Index + (subperiodChunk_len - 1))))
            #             curr_Index += subperiodChunk_len
            #         continue
            #     curr_Index += periodChunk_len
            # print(len(fixationPeriods))
            # # print(fixationPeriods)
            
        else:
            print("Could not read file: ", gazeFile, ".")
            return None

        return gazeData