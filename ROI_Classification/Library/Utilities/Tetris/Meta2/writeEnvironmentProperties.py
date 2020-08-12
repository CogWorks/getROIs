# File contains code to create json files that contain information about location
# of various objects in a tetris environment [inormation in pixels] for a 1080p screen.
# For every object in the environment, the bounding box has been calculated by:
#   Getting the extreme left/right, top/bottom coordinates followed by
#   a padding of 50 pixels (lingth of the side of each block) around the bounding box.
#   This is done to correct for error.
# The touples are (x, y) coordinates calculated with top-left corner of the screen as origin

properties = {}

# properties["resolution_width"] = 1920
# properties["resolution_height"] = 1080
# properties["block_side_length"] = 50
# properties["board_TopLeft"] = (665, 0)
# properties["board_BottomRight"] = (1305, 1080)
# properties["nextBox_TopLeft"] = (1435, 170)
# properties["nextBox_BottomRight"] = (1820, 630)
# properties["score_TopLeft"] = (145, 175)
# properties["score_BottomRight"] = (405, 370)
# properties["level_TopLeft"] = (145, 370)
# properties["level_BottomRight"] = (405, 565)
# properties["lines_TopLeft"] = (145, 565)
# properties["lines_BottomRight"] = (405, 760)

properties["resolution_width"] = 1920
properties["resolution_height"] = 1080
properties["block_side_length"] = 52
properties["board"] = {"TopLeft": (725, 20), "BottomRight": (1245, 1060)}
properties["nextBox"] = {"TopLeft": (1450, 170), "BottomRight": (1800, 620)}
properties["score"] = {"TopLeft": (145, 175), "BottomRight": (405, 370)}
properties["level"] = {"TopLeft": (145, 370), "BottomRight": (405, 565)}
properties["linesCleared"] = {"TopLeft": (145, 565), "BottomRight": (405, 760)}

import json

with open('../../../Environment/Tetris/Meta2/Meta2Properties.json', 'w') as fp:
    json.dump(properties, fp)
