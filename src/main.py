#Run this file by its self to test for facial detection with a static image
from scipy.spatial import distance as dist
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
frameRate =  60
isAlive = False

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 48
COUNTER = 0

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

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

	COUNTER = 0
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

			# extract the left and right eye coordinates, then use the
			# coordinates to compute the eye aspect ratio for both eyes
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)

			# average the eye aspect ratio together for both eyes
			ear = (leftEAR + rightEAR) / 2.0

			# compute the convex hull for the left and right eye, then
			# visualize each of the eyes
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
			
			#Check if the person is drowsy
			# check to see if the eye aspect ratio is below the blink
			# threshold, and if so, increment the blink frame counter
			if ear < EYE_AR_THRESH:
				COUNTER += 1

				# if the eyes were closed for a sufficient number of
				# then sound the alarm
				if COUNTER >= EYE_AR_CONSEC_FRAMES:
					alertUser = True
					cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), 
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
			
			# otherwise, the eye aspect ratio is not below the blink
			# threshold, so reset the counter and alarm
			else:
				COUNTER = 0

                #alerts.alert_value(alertUse)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
                        isAlive = False
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
