from scipy.spatial import distance as dist
from imutils import face_utils
import time

# constant to define the aspect ratio to indicate
# a blink
EYE_AR_THRESH = 0.26

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

# How many frames the eyes have been closed for
# reduce false positives by requireing a minimum number of frames
# for the eyes to be closed in in a row.
eyesClosed = 0

# If the eyes are detected closed
closed = True

# Holds the number of blinks in 60, 1 second slots
minute = [0]*60

# Value of the previous frame, used to reset slot in 'minute' to 0
previousFrame = 0

average_ear = 0.0
ear_frames = 0

def checkBlink(shape):
	global eyesClosed, minute, closed, previousFrame, average_ear, ear_frames, EYE_AR_THRESH
	
	# calculate the current frame/slot in increments of 60
	frame = time.localtime().tm_sec

	# Check if in new frame and remove current frame if true
	if frame != previousFrame:
		minute[frame] = 0
	previousFrame = frame

	# extract the left and right eye coordinates, then use the
	# coordinates to compute the eye aspect ratio for both eyes
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]
	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)

	# average the eye aspect ratio together for both eyes
	ear = (leftEAR + rightEAR) / 2.0

	#print(ear)

	# Check blink true if eyes are closed for more than 5 frames and then
	# open for more than 3, consecutivly. 			
	if ear < EYE_AR_THRESH:
		if closed == False:
			eyesClosed += 1
			if eyesClosed >= 3:
				eyesClosed = 0
				closed = True
	else:
		if closed == True:
			eyesClosed -= 1
			if eyesClosed < -3:
				closed = False
				eyesClosed = 0
				# increase blink count in correct slot
				minute[frame] += 1

	#Adjust the EYE_AR_THRES to accomidate eyes squinting or opening
	average_ear *= ear_frames
	if ear_frames > 500:
		ear_frames = 0
		average_ear = 0
	average_ear += ear
	ear_frames += 1
	average_ear /= ear_frames
	EYE_AR_THRESH = average_ear - 0.03

	# return total blink in the minute
	total = sum(minute)
	return total