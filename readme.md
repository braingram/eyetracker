## Coxlab Eye Tracker Project

The code contained in this repository implements a self-calibrating eyetracker
as described in the following paper:

Davide F. Zoccolan, Brett J. Graham, David D. Cox (2010) **A self-calibrating, camera-based eye tracker for the recording of rodent eye movements.** Frontiers in Neuroscience 4.

Please see [http://www.rowland.harvard.edu/cox/pdfs/fnins-04-00193-1.pdf](http://www.rowland.harvard.edu/cox/pdfs/fnins-04-00193-1.pdf) for details.


## Installation instructions

**NOTE: these instructions are a work in progress, so please let us know if you run into trouble, so that we can improve the documentation of this process**

The software has so far only been tested and used on Mac OS X, though it should work, in principle, on any platform.  Please contact us if you have success in running it on other platforms.

Assuming you have a complete, working Python install, installing the program should be as easy as downloading the code and running
    
    python setup.py install
    
Alternatively, you could skip downloading the code and try (assuming you have pip installed, which you should):

    pip install -e git+https://github.com/coxlab/eyetracker#egg=coxlab_eyetracker

The tracker can then be run from a shell with the command

    coxlab_eyetracker

Depending on the state of your Python install, you might run into a few problems.  First, you'll need the `distribute` module.  You can install this by running the `distribute_install.py` script included in this distribution.

You'll also need scipy and numpy and a host of other Python modules.  Since these can be tricky to install for new users, we recommend downloading the Enthought Python Distribution, which is a complete, batteries-included, free-for-academics Python distribution.  
