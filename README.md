# rigol-scopegui
A GUI application for controlling oscilloscopes over the network (tested on RIGOL MSO1000Z series)

It can display the signals being measured by the oscilloscope and change the most common settings.

EXECUTE gui.py TO RUN ("python3 gui.py" in CLI or just make it executable)

Dependencies:

Python 3   (>=3.1)

PyQt4      (>=4.9)

pyqtgraph  (>=0.9.9)

vxi11      (included in files)

This is a GUI application I threw together as a school project.
The code is quite messy but i put it up for anyone to try it out.
It is capable of controlling oscilloscopes over the network using IPv4.
It was tested on a RIGOL MSO1074Z-S oscilloscope so it should work on the DS/MSO1000Z series.
I also briefly tested it on an MSO2072A and it worked fine (except channel 3 and 4 since it's a 2 channel scope) so it might work whit others as well.
I tested it on Debian, Ubuntu and Fedora tho it should work on any OS that supports it's dependencies.
