# ROI_Classification
Contains code for combining gaze data (gazetools csv output) and game data to produce ROI classifications.

- The main code (that calls all other packages in the project) should be located at the root (directly under getROIs/ROI_Classification/).
- You can use 'getROIs/ROI_Classification/getROI_CTWC19.py' as a guide on how to call functions and classes in the project (under the library directory) to perform ROI classification.
- NOTE: If you contribute to the project and add more code, make sure you are creating the correct package and sub-package structure. And be sure to make it as modular as possible so changes would not requre, modifying any code rather writing one's own module and calling it instead of existing modules.


# Project Structure

- Library
	- DataClasses : Contains class structures that store game and gaze data.
	- Environment : Contains environment specific information like: bounding boxes (xy-coordinates) of static objects in the scene (JSON file). The code uses this information to find overlap of fixation locations with provided bounding locations to determine fixations at static locations.
		- The bounding regions contain the xy-coordinates (in pixels) of the top-left and bottom-right corner of the bounding box for each static object in the scene.
	- Parsers : Contains code to parse (input) csv files, convert them into DataClass(es) and return these objects for these classes containing the data from the file parsed.
	- ROI_Codes : Contains the code that actually performs the ROI-classification.
		- ROI_Logic.py : This is the heart of the project, it performs the actual classification. It requires
			- The static bounding regions for all objects in the scene passed as a dictionary.
			- the dynamic bounding region for objects in the scene at each timestamp.
			- The gaze locations at each time stamp.
			- Other parameters are necessary. The file contains detailed description of each parameter.
			- Returns a pandas dataframe containing the timestamp for the start and end of the fixation periods along with the element being fixated on (The name depends on the dictionary key for the static objects and column name for the dynamic objects)
		- GenerateROI_Meta2.py : sample code that demonstrates how to prepare the data and call ROI_Logic to perform the classification.
	- Utilities : Contains other important functions necessary for processing data, examples include:
		- Tetris/Meta2/CTWC19_Utils.py : Contains logic for aligning game (Meta-TWO) and gaze (Tobii-Spectrum) data that were collected during CTWC19, since there was no way to synchronize these files automatically at the time. 
		- writeEnvironmentProperties.py : Contains code, that creates a dictionary for the list of static regions in a Meta-Two game on a 1080p screen and writes it out as a JSON file.



# Not currently thought out (Currently Ignore)

## Coming soon:
- Compatibility with other gaze inputs or other game style inputs
	- such as MetaT
	- such as JAG
- Propagation of uncertainty
	- allows for probabilistic approach
	- Appropriate for more ambiguous gaze environments, like JAG
	- Allows for partial association with multiple gaze objects
		
## Simple getROIS tsv outputs with one subjects' data:
- Will write ROI-classified gaze data to same directory as eyeFile data
- You need:
	- Python 3.8+ installed
	- Data for subject
		- Meta2 Files in one directory
			- 1 game file per game
			- Game names like: 19CTWC007_2019-10-19_06-28-54_classic-tetris_zerotillnineteen.tsv
			- Log file like:  191019-061931_19CTWC007_SPEEDTETRIS.log
			- Sync File like: 191019-061931_19CTWC007_SPEEDTETRIS_tobii-sync.tsv
		- Gazetools output file
			- should have used Tobii file as input to Gazetools
			- Tobii names like: CTWC19 Recording8 19CTWC007
	- getROIS
- Can call from command line or in file:
	- Command line: `python writeROIs.py logFile eyeFile`
	- in Python: `writeROIs(logFile, eyeFile)
	- where `logFile` is the location of the Meta2 log file
	- where `eyeFile` is the location of the gazetools eye file
	
	
	
	
