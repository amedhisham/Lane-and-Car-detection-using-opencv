opencv and ultralytics/yolo needed to run project.

Entry point is main.py.

When an image window pops up, the window needs to be closed manually for the script to proceed.

During car detection, after closing the image window the detection info gets printed in the terminal. 
This can be confusing because the next car image window will pop up next but the info in the terminal refers to the last closed image not to the active one
