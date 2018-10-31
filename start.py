# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main
main.main(webcamSource)