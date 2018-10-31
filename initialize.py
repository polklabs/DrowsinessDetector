#Returns id of webcam to be used
#Else exits the program

#Other imports we use will be added and checked in here
def initialize():
	print("INITIALIZING PYTHON AND MODULES")

	#Checking python version
	import sys
	print("Checking python version:")
	if sys.version_info[0] > 2 or sys.version_info[0] < 2:
		#raise Exception("Must be using Python 2.7")
		print("Must be using python 2.7")
		sys.exit(1)
	else:
		print("OK\n")

	#Checking opencv
	print("Checking OpenCV version:")
	try:
		import cv2
		print("OpenCV version: "+str(cv2.__version__)+"\n")
	except ImportError:
		print("Could not import OpenCV.")
		sys.exit(1)

	#Check webcam
	print("Checking for valid webcam:")
	import cv2
	def testDevice(source):
		cap = cv2.VideoCapture(source)
		if cap is None or not cap.isOpened():
			return False
		return True

	for i in range(2):
		if testDevice(i):
			print("OK\nUsing webcam "+str(i)+"\n")
			return i
	print("Could not find a valid webcam")
	sys.exit(1)