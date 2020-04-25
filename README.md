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
		
