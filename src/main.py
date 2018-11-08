#Run this file by its self to test for facial detection with a static image

from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import cv2 #For image processing
import time #for timeing frame rate
import dlib #For detecting faces and features

import alerts
import isDrowsy #For testing

test = False
testFailed = 0

shape_predictor_file = "shape_predictor_68_face_landmarks.dat"
frameRate =  4

#Grabs frame from the video source
def grabFrame(vs):
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	return frame

#Opens image for testing
def grabTestFrame():
	img = cv2.imread("testFace.jpg",1)
	frame = np.array(img)
	frame = imutils.resize(frame, width=450)
	return frame

#Draw a box over the face in the displayed feed
def drawBox(frame, rect):
	x1, y1, x2, y2, w, h = rect.left(), rect.top(), rect.right() + 1, rect.bottom()+1, rect.width(), rect.height()
	cv2.rectangle(frame, (x1,y1),(x2,y2), (255, 0, 0), 2)
	return frame

#Draws words on the image if no face is detected
def noFace(frame):
	cv2.putText(frame, "NO FACE DETECTED!", (10, 30), 
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

def main(webcamSource):
	# initialize dlib's face detector (HOG-based) and then create
	# the facial landmark predictor
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(shape_predictor_file)

	# start the video stream thread
	print("[INFO] starting video stream thread...")
	vs = VideoStream(webcamSource).start()
	time.sleep(1.0)

	while True:
		start_time = time.time()

		alertUser = False

		frame = grabFrame(vs)
		if test:
			if type(frame) is np.ndarray:
				print("[TEST] Frame grab: passed")
			else:
				print("[TEST] Frame grab: failed")
				testFailed += 1
			frame = grabTestFrame()


		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		#Get the faces in the image
		rects = detector(gray, 0)

		if len(rects) is 0:
			noFace(frame)
			if test:
				testFailed += 1
				print("[TEST] Face detection: failed")

		#Iterate over the faces
		for rect in rects:
			if test:
				print("[TEST] Face detection: passed")

			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)

			frame = drawBox(frame, rect)

			#Check if the person is drowsy
			if isDrowsy.isDrowsy(shape):
				alertUser = True
				cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), 
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

		alerts.Alert.alert_value(alertUser)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break

		#Determine how long if at all the program should wait before continuing
		elapsed_time = time.time() - start_time
		time_left =(1.0/frameRate)-elapsed_time 
		if time_left > 0:
			time.sleep(time_left)

		if test:
			vs.stop()
			return

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

if __name__ == "__main__":
	import sys

	test = True
	main(0)
	print("[INFO] Tests finished")
	print("[RESULT] "+str(testFailed) + " tests failed.")
	print("\nWaiting 30 seconds to close window...")
	time.sleep(30)
	cv2.destroyAllWindows()
	sys.exit(0)