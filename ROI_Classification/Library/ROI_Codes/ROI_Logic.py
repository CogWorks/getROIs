import pandas as pd
from itertools import groupby

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


"""
Generates classified information about gaze fixation element in the environment over time
Takes as input a Pandas DataFrame with the following Structure :
        1. First column is for the timestamp: timestamp.
        2. Next 5 columns for gaze information: gazeX, gazeY, gazeZ, gazeClass, gazeEventID.
            2.1. gazeClass can have values: blink, fixation, saccade, glissade-slow, glissade-fast, noise.
        3. All following columns represent the bounding area of dynamic elements on the screen at the time, \
           each in the form of a list of 2 touples, each tuple an (X,Y) coordinate for the: \
			3.1. Top-Left corner of the boundig box
			3.2. Bottom-Right corner of the bounding box
"""
class ROI_Classifier:
	"""
	:param staticRegionsDict: Dictionary containing locations (coodinates of top-right and bottom-left corners) \
								of bounding box of all static objects on the screen. The dictionary structure involves \
								names of static regions as keys each of which have dictionaries as values with keys \
								'TopLeft' & 'BottomRight' each with a tuple values of the (X,Y) corrdinates of the two \
								corners of the object.
	:param staticRegionNames: key values of the static regions in staticRegionsDict.
	Other local-variables:
	staticPolygonsDict: a dictionary of Polygon objects (from shapely library) for each region of interest
	"""
	def __init__(self, staticRegionsDict, staticRegionNames):
		# self.staticRegionsDict = staticRegionsDict
		self.staticRegionList = staticRegionNames
		self.staticPolygonsDict = {}
		for regionName in staticRegionNames:
			top = staticRegionsDict[regionName]["TopLeft"][1]
			left = staticRegionsDict[regionName]["TopLeft"][0]
			bottom = staticRegionsDict[regionName]["BottomRight"][1]
			right = staticRegionsDict[regionName]["BottomRight"][0]
			self.staticPolygonsDict[regionName] = Polygon([(left, top), (left, bottom), (right, bottom), (right, top)])


	"""
	:param dataDF: Pandas dataframe containing all data
	:param syncDelayTolerance: 
	:param frequency: Frequency of data recording in milliseconds (Default: is set to ms value corresponding to 60Hz)
	"""
	def classifyROI_byGaze(self, dataDF, syncDelayTolerance = 0, frequency = 16.6):
		print("Began Classification")

		# Remove all blinks and noise
		modifiedDF = dataDF[(dataDF.gazeClass != 'blink') & (dataDF.gazeClass != 'noise')]
		# print(len(modifiedDF))
		# print(modifiedDF[pd.isna(modifiedDF.gazeX)])

		# Split data into periods of fixations
		curr_Index = 0
		fixationPeriods = []
		append = fixationPeriods.append
		for currPeriod, periodChunk in groupby(modifiedDF.gazeClass.tolist()):
			periodChunk_len = len(list(periodChunk))
			if currPeriod.lower() == 'fixation':
				# print(curr_Index)
				# Divide each fixation chunk into multiple events (each for a different fixation), if exists
				subEvents = modifiedDF.iloc[curr_Index : (curr_Index + (periodChunk_len - 1))].gazeEventID.tolist()
				for currSubperiod, subperiodChunk in groupby(subEvents):
					subperiodChunk_len = len(list(subperiodChunk))
					if subperiodChunk_len > 2:
						append((curr_Index, (curr_Index + (subperiodChunk_len - 1))))
					curr_Index += subperiodChunk_len
				continue
			curr_Index += periodChunk_len
		print("Number of fixations found: ", len(fixationPeriods))
 
		# To get percentage of successful fixation-bindings
		totalFixations = len(fixationPeriods)
		fixationOverlapsFound = 0

		# Classify fixation regions
		ROI_list = []
		append = ROI_list.append
		for periodIndices in fixationPeriods:
			# Get start and end row indices for current fixation period
			periodStart = periodIndices[0]
			periodEnd = periodIndices[1]

			# If there's a difference of greater than 20 pixels between fixations, it is likely two different fixations
			if (abs(modifiedDF.iloc[periodStart]["gazeX"] - modifiedDF.iloc[periodEnd]["gazeX"]) > 20) or \
				(abs(modifiedDF.iloc[periodStart]["gazeY"] - modifiedDF.iloc[periodEnd]["gazeY"]) > 20):
					continue

			# Get current gaze location as a shapely point object
			currGazeLocation = Point(modifiedDF.iloc[periodStart:periodEnd]["gazeX"].mean(axis=0), \
										modifiedDF.iloc[periodStart:periodEnd]["gazeY"].mean(axis=0))
			
			# Debug Stuff
			# print(periodStart, periodEnd)
			# print(modifiedDF.iloc[periodStart]["gazeX"], modifiedDF.iloc[periodEnd]["gazeX"], modifiedDF.iloc[periodStart:periodEnd]["gazeX"].mean(axis=0))
			# print(modifiedDF.iloc[periodStart]["gazeY"], modifiedDF.iloc[periodEnd]["gazeY"], modifiedDF.iloc[periodStart:periodEnd]["gazeY"].mean(axis=0))

			# Check static regions for overlap
			inStaticRegion = False
			for region, regionPolygon in self.staticPolygonsDict.items():
				if regionPolygon.contains(currGazeLocation):
					inStaticRegion = True
					break

			# Check dynamic regions for overlap
			inDynamicRegion = False
			if not inStaticRegion:
				for columnIndex in range(6, len(modifiedDF.columns)):
					# Find closest non-Null dynamic-object locations
					# print(periodStart, periodEnd)
					currPeriodStart = periodStart
					while (modifiedDF.iloc[currPeriodStart][columnIndex] is None) and (currPeriodStart < periodEnd):
						currPeriodStart += 1
					currPeriodEnd = periodEnd
					while (modifiedDF.iloc[currPeriodEnd][columnIndex] is None) and (currPeriodEnd > periodStart):
						currPeriodEnd -= 1
					# print(currPeriodStart, currPeriodEnd)
					if (currPeriodStart >= currPeriodEnd):
							continue
					# Check first frame of fixation
					top = modifiedDF.iloc[currPeriodStart, columnIndex][0][1]
					left = modifiedDF.iloc[currPeriodStart, columnIndex][0][0]
					bottom = modifiedDF.iloc[currPeriodStart, columnIndex][1][1]
					right = modifiedDF.iloc[currPeriodStart, columnIndex][1][0]
					if Polygon([(left, top), (left, bottom), (right, bottom), (right, top)]).contains(currGazeLocation):
						inDynamicRegion = True
						break
					# Check last frame of fixation
					top = modifiedDF.iloc[currPeriodEnd, columnIndex][0][1]
					left = modifiedDF.iloc[currPeriodEnd, columnIndex][0][0]
					bottom = modifiedDF.iloc[currPeriodEnd, columnIndex][1][1]
					right = modifiedDF.iloc[currPeriodEnd, columnIndex][1][0]
					if Polygon([(left, top), (left, bottom), (right, bottom), (right, top)]).contains(currGazeLocation):
						inDynamicRegion = True
						break

			if inStaticRegion:
				append([modifiedDF.iloc[periodStart]["timeStamp"], modifiedDF.iloc[periodEnd]["timeStamp"], region])
				fixationOverlapsFound += 1
			elif inDynamicRegion:
				append([modifiedDF.iloc[periodStart]["timeStamp"], modifiedDF.iloc[periodEnd]["timeStamp"], modifiedDF.columns[columnIndex]])
				fixationOverlapsFound += 1
			else:
				append([modifiedDF.iloc[periodStart]["timeStamp"], modifiedDF.iloc[periodEnd]["timeStamp"], 'blank-stare'])

		print("{:.2%} of all fixations overlapped with objects.".format((fixationOverlapsFound/totalFixations)))
		ROI_DF = pd.DataFrame(ROI_list, columns=['fixation_startTime', 'fixation_endTime', 'fixation_Element'])
		print("Classification Complete")
		return ROI_DF