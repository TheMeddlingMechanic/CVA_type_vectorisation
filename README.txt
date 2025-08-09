To use this, run main.py with python, following the instructions, pressing ENTER (or any other key of your choice) to move on when prompted.

CVA is a vector image filetype made of polygons filled with colour called "contours".

You can select a CVA file or a normal image file.
If it was a CVA, it will simply display.
If it was another type of image, it will be converted to a CVA.

You can choose to save the final CVA to a file, in which case it can later be accessed by choosing
the new saved CVA file at the start of the running the program.

If you'd like, you can mess with the settings in the VectoriseStep.py file -- particularly the paramater for do_thresh() (I've found that 30 gets nice results while still being fairly efficient).