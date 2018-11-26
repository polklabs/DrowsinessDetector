from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import cv2 #For image processing
import time #for timeing frame rate
import dlib #For detecting faces and features

import alerts

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.3

MOUTH_AR_THRESH = 0.4

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
	eye_ar = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return eye_ar

def eyesClosed(shape):

	# extract the left and right eye coordinates, then use the
	# coordinates to compute the eye aspect ratio for both eyes
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]
	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)

	# average the eye aspect ratio together for both eyes
	eye_ar = (leftEAR + rightEAR) / 2.0

	# compute the convex hull for the left and right eye, then
	# visualize each of the eyes
	#leftEyeHull = cv2.convexHull(leftEye)
	#rightEyeHull = cv2.convexHull(rightEye)
	#cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
	#cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
			
	#Check if the person is drowsy
	# check to see if the eye aspect ratio is below the blink
	# threshold, and if so, increment the blink frame counter
	if eye_ar < EYE_AR_THRESH:
		return True
		
def mouthOpen(shape):
	mouthTop = shape[51]
	mouthBot = shape[57]
	mouthLeft = shape[54]
	mouthRight = shape[48]
	
	A = dist.euclidean(mouthTop, mouthBot)
	B = dist.euclidean(mouthLeft, mouthRight)
	
	mouth_ar = (A) / (2.0 * B)
	
	if mouth_ar > MOUTH_AR_THRESH:
		return True
	
	
	