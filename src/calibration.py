## calibration step for new user account

from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
import numpy as np
import imutils
import cv2 #For image processing
import time #for timeing frame rate
import dlib #For detecting faces and features

shape_predictor_file = "shape_predictor_68_face_landmarks.dat"

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#Grabs frame from the video source
def grabFrame(vs):
	frame = vs.read()
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

def main():
	global test, testFailed

	# initialize dlib's face detector (HOG-based) and then create
	# the facial landmark predictor
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(shape_predictor_file)

	# start the video stream thread
	print("[INFO] starting video stream thread...")
	vs = VideoStream(0).start()
	time.sleep(1.0)

	EYE_COUNTER = 0
	MOUTH_COUNTER = 0
	totalFrames = 0
	x = 0
	totalEyeAspectRatio = 0.0
	totalMouthAspectRatio = 0.0

	while x < 200:

		frame = grabFrame(vs)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


		cv2.putText(frame, "Blink normally and keep mouth open", (10, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
		if x == 0:
			time.sleep(10)
				
				
		#Get the faces in the image
		rects = detector(gray, 0)

		if len(rects) is 0:
			noFace(frame)

		if len(rects) > 1: 
			multipleFace(frame)
		
		else:
			#Iterate over the faces
			for rect in rects:

				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)

				# extract the left and right eye coordinates, then use the
				# coordinates to compute the eye aspect ratio for both eyes
				leftEye = shape[lStart:lEnd]
				rightEye = shape[rStart:rEnd]
				leftEAR = eye_aspect_ratio(leftEye)
				rightEAR = eye_aspect_ratio(rightEye)

				# average the eye aspect ratio together for both eyes
				ear = (leftEAR + rightEAR) / 2.0
				totalEyeAspectRatio = totalEyeAspectRatio + ear
				x = x + 1
				frame = drawBox(frame, rect)

				# extract mouth coordinates
				mouthTop = shape[51]
				mouthBot = shape[57]
				mouthLeft = shape[54]
				mouthRight = shape[48]

				A = dist.euclidean(mouthTop, mouthBot)
				B = dist.euclidean(mouthLeft, mouthRight)

				mouth_ar = (A) / (2.0 * B)
				totalMouthAspectRatio = totalMouthAspectRatio + mouth_ar


		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break
				
	averageEyeAspectRatio = totalEyeAspectRatio/200
	averageMouthAspectRatio = totalMouthAspectRatio/200
	print(averageEyeAspectRatio)
	print(averageMouthAspectRatio)
		
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	return [averageEyeAspectRatio, averageMouthAspectRatio]
	# do a bit of cleanup
	# cv2.destroyAllWindows()
	# vs.stop()
#main()
