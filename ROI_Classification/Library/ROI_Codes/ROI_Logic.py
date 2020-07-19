import pandas as pd

"""
Generates classified information about gaze fixation element in the environment over time
Takes a Pandas DataFrame with :
        1. First column for the timestamp: timestamp.
        2. Next 4 columns for gaze information: gazeX, gazeY, gazeZ, gazeClass.
        3. All following columns represent the bounding area of dynamic elements on the screen at the time, \
           each in the form of a list of 2 touples, coordinates (X,Y) for the: \
                3.1. Top-Left corner of the boundig box
                3.2. Bottom-Right corner of the bounding box
           Each tuple is 
"""
class ROI_Classifier:
        """
        :param staticRegionsDict: Dictionary containing locations (coodinates of top-right and bottom-left corners) \
                                  of bounding box of all static objects on the screen.
        :param dataDF: Pandas dataframe containing all data
        :param staticRegionNames: 
        """
        def __init__(self, staticRegionsDict, staticRegionNames):
                self.staticRegionsDict = staticRegionsDict
                self.staticRegionList = staticRegionNames
        
        def classifyROI_byGaze(self, dataDF, syncDelayTolerance = 0):
                print("Began Classification")
                ROI_DF = pd.DataFrame()
                # Check if (X,Y) coordinates for from gazeX and gazeY fall within the static regions
                # If they don't, check the dynamic regions at that time
                # If there is no match, categorize as blank-stare
                return ROI_DF

        def static_ROI(self):
                pass

        def dynamic_ROI(self):
                pass