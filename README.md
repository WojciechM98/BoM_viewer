# BoM_viewer
Simple GUI application to manage components for electronic projects.

At the moment this app allows to view two BoM files side by side, compare them and create new purchase lists.

Clone, create venv and run "pip install -r requirements.txt". 

It expects setting.json file to know in what order columns are in BoM files. 

Running gui.py opens tkinter windows. For testing purposes at startup two files are loaded. Top window allow you to search for value in second window (another BoM) by clicking with left mouse button on value - if the same value is found in second window it will be highlighted. Right mouse click coppy value.

There is option to save and save as files from this two windows.

Another function is to create purchase file. This acction can be done by clicking File -> Create purchase file. You will be promped to name and save file. This function compares two oppened BoM files for duplicates saving only differences. Very useful when running many electronic projects at the same time using similar components.

This app is still in developement. I am oppened for collabs!