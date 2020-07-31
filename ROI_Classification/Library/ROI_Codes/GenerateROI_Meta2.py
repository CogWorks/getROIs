from .ROI_Logic import ROI_Classifier

from pathlib import Path
import json
import numpy as np

class GetROI_Meta2:
    """
    Variables being set:
    regionBoundsDict: A JSON file specifying the location bounds for all static elements in the environment
    ClassifierObj: Instantiating the classifier object with properties common for all current games
    startCoordinates: The coordinate for the top-left cornet of the tetris board, which is the origin from where \
                            all coordinates for zoid and filled board regions are measured.
    blockSize: Length of the sides of blocks (in pixels) at a specific resolution.
    currBounds: Keeps track of the bounds for the object last processed. if a None value is encountered, bounds \
                for the last encountered object are set for the current time.
    """
    def __init__(self):
        # Open JSON file containing bounding coordinates of static elements in the environment
        path = Path(__file__).parent / "../Environment/Tetris/Meta2/Meta2Properties.json"
        self.regionBoundsDict = json.load(path.open())
        # Create a classifier object for all games
        self.ClassifierObj = ROI_Classifier(self.regionBoundsDict, ["nextBox", "score", "level", "linesCleared"], \
                                            ['zoid', 'pile'])
        # Variables necessary for binaryRep_2_boundingCoordinates function
        self.blockSize = self.regionBoundsDict["block_side_length"]
        self.currBounds = None
        self.currRepresentation = None
        boardCoordinates = self.regionBoundsDict["board"]
        self.boardWidth = boardCoordinates["BottomRight"][0] - boardCoordinates["TopLeft"][0]
        self.boardHeight = boardCoordinates["BottomRight"][1] - boardCoordinates["TopLeft"][1]
        # startCoordinates are the coordinates of the top-left corner of the board treated as the origin
        # for the dynamic regions
        self.startCoordinates = self.regionBoundsDict["board"]["TopLeft"]

    
    """
    Takes input board and zoid representations from meta2 Data and converts them into tuples of (X,Y) coordinates of \
        top-left and bottom right corner of bounding boxes (a rectangle that contains the zoid or the filled in board, \
        padded by one block) for the objects in the representations.
    Parameters:
    :param representation: the board/zoid representation of the tetris board at a specific time
    :return: The top-left and bottom-right corner coordinates for the bounding box of the zoid or filled board regions.
    """
    def binaryRep_2_boundingCoordinates(self, representation):
        # If empty or repeated representation return previous result
        if representation == None or representation == self.currRepresentation:
            # print("Got empty representation")
            return self.currBounds
        else:
            self.currRepresentation = representation

        # Get rid of all '0' elements
        # sparseRepresentation = sparse.csr_matrix(representation)

        # (nonEmpty_rows, nonEmpty_cols) = sparseRepresentation.nonzero()
        (nonEmpty_rows, nonEmpty_cols) = np.array(representation).nonzero()
        if len(nonEmpty_cols) == 0 or len(nonEmpty_rows) == 0:
            # Cases when board is empty, due to all lines cleared
            self.currBounds = [(0, 0), (0, 0)]
            return self.currBounds

        # Create local variable for efficiency
        blockSize = self.blockSize
        startCoordinates = self.startCoordinates

        left_border = max((min(nonEmpty_cols) - 1) * blockSize, 0)
        right_border = min((max(nonEmpty_cols) + 2) * blockSize, self.boardWidth)
        top_border = max((min(nonEmpty_rows) - 1) * blockSize, 0)
        bottom_border = min((max(nonEmpty_rows) + 2) * blockSize, self.boardHeight)

        bound_topLeft = (startCoordinates[0] + left_border, startCoordinates[1] + top_border)
        bound_bottomRight = (startCoordinates[0] + right_border, startCoordinates[1] + bottom_border)

        self.currBounds = [bound_topLeft, bound_bottomRight]
        return self.currBounds


    """
    Converts the current data into a format that is supported by the ROI Classifier
    Parameters:
    :param dataDF: Pandas DataFrame containing aligned game and gaze data with location of all dynamic objects along each axis \
                    and corresponding gaze location at the time
    :param syncDelayTolerance: In case of possibility of misalignment of game and gaze files, it is going to check in a window of the \
                                number of milliseconds in value passed. (Sign Sensitive)
                                Ex: if 500 is passed, then it will check for any correspondence of the current gaze location with \
                                    upto the next 500ms for any object in the game file, and previous 500ms for a value of -500.
    :return: Pandas DataFrame containing timeStamp and the name of the element being fixated at.
    Deprecated:
    :param dynamicObjectColumns: List of column names that contain information about dynamic objects in the environment
    :param gazeInformationColumns: List of column names that contain information about the X, Y and Z coordinate of gaze respectively
    """
    def generateROIClassification(self, dataDF, syncDelayTolerance = 0):
        print("Converting Data for ROI Classification")

        # Prepare dataframe passing to ROI Classifier
        # print(binaryRep_2_boundingCoordinates(test["board"]["TopLeft"], test["block_side_length"], dataDF["zoidRep"][4]))
        dataDF['zoid'] = dataDF['zoidRep'].apply(self.binaryRep_2_boundingCoordinates)
        dataDF['pile'] = dataDF['boardRep'].apply(self.binaryRep_2_boundingCoordinates)

        # Drop all columns except those necessary for ROI
        keepCols = ['timeStamp', 'gazeX', 'gazeY', 'gazeZ', 'gazeClass', 'gazeEventID', 'zoid', 'pile']
        dropList = list(set(dataDF.columns) - set(keepCols))
        dataDF.drop(columns=dropList, inplace = True)

        print("Convertion Complete")

        return self.ClassifierObj.classifyROI_byGaze(dataDF, syncDelayTolerance)