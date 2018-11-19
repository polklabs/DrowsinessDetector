# DrowsinessDetector

### Abstract
Our program aims to alert users if they are drowsy by analyzing video input from a webcam. The intended use for Aerospace is for mission control workers to stay alert, as launches may occur at any time.

## Guide
A breakdown of the the files under our source code directory
* **alerts.py** - alerts module that contains alert function using alert.wav in assets/
* **isDrowsy.py** - primary drowsiness analysis module that will contain multiple functions to perform on faces
* **main.py** - main module defines frame grabbing functions and uses them to perform analysis with video input
* **shape_predictor_68_face_landmarks.dat** - data file used by dlib library to detect facial landmarks
* **initialize.py** - module that checks for crucial dependencies of Python version, OpenCV version, and webcam validity, returning the webcam if valid
* **start.py** - starting module calls on initialize() to retrieve the webcam, then calls the main function on the webcam
* **testFace.jpg** - image of Ryan Reynolds used to test facial analysis

## Dependencies
+ Python
+ OpenCV
+ Dlib
+ Additional python modules associated with dlib, OpenCV, and sounds
