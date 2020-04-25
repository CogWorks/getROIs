# getROIs
Turns Cogworks/gazetools gaze data and Meta2 game data into ROI-classified gaze data.

## Inputs:
- classified gaze data (rda or csv)
	- gaze location
	- gaze classification
- game files = collections of game events:
	- Episodes
	- zoid_rep
	- board_rep
- linkage method for gaze and game data
	- Time stamp glue file
	- (Tobii Sync tsv for Meta2)

## Outputs:
ROI-classified gaze data for duration of participant gaze
- collection of ROI-classified gaze objects
- a gaze object has:
	- timestamps
	- time series of gaze location
	- association with game object such as:
		- curr_zoid
		- placement_location
		- Next_box

## Coming soon:
- Compatibility with other gaze inputs or other game style inputs
	- such as MetaT
	- such as JAG
- Propagation of uncertainty
	- allows for probabilistic approach
	- Appropriate for more ambiguous gaze environments, like JAG
	- Allows for partial association with multiple gaze objects
		
# Simple getROIS tsv outputs with one subjects' data:
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
	
	
	
	
