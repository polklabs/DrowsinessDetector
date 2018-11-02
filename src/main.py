import cv2
import time
import isDrowsy

def main(webcamSource):
    #This is place holder code -------------------
    print("Running main code of project.")
    
    cap = cv2.VideoCapture(webcamSource)
    print("Press \'q\' to exit.")

    while(True):
        start_time = time.time()
        
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if isDrowsy.isDrowsy():
            print("Drowsy")
        else:
            print("Not Drowsy")
        #Runs the webcam at 1 fps
        elapsed_time = time.time() - start_time
        time_left =1-elapsed_time 
        if time_left > 0:
            time.sleep(time_left)
    cap.release()
    cv2.destroyAllWindows()
    #----------------------------------------------
