# Class to run a subprocess that handles opening the webcam

import main
import initialize

webcamSource = initialize.initialize()
main.main(webcamSource)