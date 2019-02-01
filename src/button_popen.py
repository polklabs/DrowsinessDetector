# Class to run a subprocess that handles opening the webcam

import main
import sys

if __name__ == '__main__':
    webcamSource = int(sys.argv[1])
    username = sys.argv[2]
    password = sys.argv[3]
    main.main(webcamSource,username,password)