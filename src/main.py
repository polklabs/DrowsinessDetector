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
import blinkFreq
import time
import firebase_login

testing = False
test = 0
testFailed = 0

shape_predictor_file = "shape_predictor_68_face_landmarks.dat"
frameRate =  30

EYE_AR_CONSEC_FRAMES = 48
MOUTH_AR_CONSEC_FRAMES = 30

#Grabs frame from the video source
def grabFrame(vs):
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	return frame

#Opens image for testing
def grabTestFrame():
	img = ''
	if test == 1:
		img = cv2.imread("testFace.jpg",1)
	if test == 2:
		img = cv2.imread("testFace2.jpg", 1)
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

def multipleFace(frame):
	cv2.putText(frame, "MULTIPLE FACES DETECTED", (10, 30), 
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

def main(webcamSource,username,password):
	global test, testFailed
	user = firebase_login.signIntoFirebase(username,password)
	#print(firebase_login.getUserData(username,user))
	# initialize dlib's face detector (HOG-based) and then create
	# the facial landmark predictor
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(shape_predictor_file)

	# start the video stream thread
	print("[INFO] starting video stream thread...")
	vs = VideoStream(webcamSource).start()
	time.sleep(1.0)

	alertUser = False
	#sentAlert = False

	startTime = time.localtime().tm_min
	minutePassed = False

	EYE_COUNTER = 0
	MOUTH_COUNTER = 0
	totalFrames = 0
	while True:
		start_time = time.time()

		frame = grabFrame(vs)
		if testing:
			if type(frame) is np.ndarray:
				print("[TEST] Frame grab: passed")
			else:
				print("[TEST] Frame grab: failed")
				testFailed += 1
			frame = grabTestFrame()

		frame = cv2.flip(frame, 1)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		

		#Get the faces in the image
		rects = detector(gray, 0)

		if len(rects) is 0:
			noFace(frame)
			if test:
				testFailed += 1
				print("[TEST] Face detection: failed")

		if len(rects) > 1: 
			multipleFace(frame)
			if test:
				testFailed += 1
				print("[TEST] Face detection: failed")
		
		else:
			#Iterate over the faces
			for rect in rects:
				if test:
					print("[TEST] Face detection: passed")

				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)

				#Get blink rate and print on shown image
				rate = blinkFreq.checkBlink(shape)
				if minutePassed is False:
					if time.localtime().tm_min - startTime >= 1:
						minutePassed = True
				else:
					if rate >= 25 or rate <= 10:
						cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), 
							cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
						alertUser = True
						#Update firebase here
				cv2.putText(frame, "Blinks/min: "+str(rate), (275, 30), 
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

				frame = drawBox(frame, rect)
			
				if isDrowsy.mouthOpen(shape) == True:
					MOUTH_COUNTER += 1
				else:
					MOUTH_COUNTER = 0
			
				if isDrowsy.eyesClosed(shape) == True:
					EYE_COUNTER += 1
				else:
					EYE_COUNTER = 0
				
				if EYE_COUNTER >= EYE_AR_CONSEC_FRAMES or MOUTH_COUNTER >= MOUTH_AR_CONSEC_FRAMES:
					cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), 
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
					alertUser = True
					#Update firebase here
				#else:
				#	sentAlert = False
					#alertUser = False

		alerts.alert_value(alertUser)
		alertUser = False

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# count number of frames passed while resetting to 0 when 1 minute is reached
		totalFrames += 1
		totalFrames = totalFrames % (60*frameRate)

		#Determine how long if at all the program should wait before continuing
		elapsed_time = time.time() - start_time
		time_left =(1.0/frameRate)-elapsed_time 
		if time_left > 0:
			time.sleep(time_left)

		if testing:
			if test == 2:
				vs.stop()
				return
			if test == 1:
				time.sleep(5)
			test += 1

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

if __name__ == "__main__":
	import sys

	testing = True
	test = 1
	main(0)
	print("[INFO] Tests finished")
	print("[RESULT] "+str(testFailed) + " tests failed.")
	print("\nWaiting 5 seconds to close window...")
	time.sleep(5)
	cv2.destroyAllWindows()
	sys.exit(0)
