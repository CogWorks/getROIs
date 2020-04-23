# getROIs
Turns gaze data and game data into ROI-classified gaze data


Inputs:
	classified gaze data (rda or csv)
		gaze location
		gaze classification
		Applyable high and low pass filters
	game files = collections of game events:
		Episodes
		zoid_rep
		board_rep
	linkable together by time stamps
		and for different recording sessions
	(interface for MetaT inputs too)
	
	


Outputs:
	ROI-classified gaze data for duration of gaze
		collection of ROI-classified gaze object:
			association with game object
				curr_zoid
				placement_location
				Next_box
				etc
			time series of gaze location
			timestamps
			
	(uncertainty)
		(association with multiple gaze objects)
		
		

Other desiderata:
	Maintainable
		modular
		object-oriented
	Extendable to other gaze paradigms
		(such as JAG)
		(inclusion of uncertainty)
	Well-documented
		(to some particular specified standard)
	Work-onable by Chris and Sounak simultaneously for swift development
	
Weird things to remember:
	tobii time stamp offsets
	
