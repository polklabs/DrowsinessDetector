# Class to run a subprocess that handles opening the webcam

import main
import sys

if __name__ == '__main__':
    webcamSource = int(sys.argv[1])
    main.main(webcamSource)