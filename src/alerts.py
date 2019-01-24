from threading import Thread
import playsound

isPlaying = False
hasStarted = False

def sound_alarm(path):
    global isPlaying
    while True:
        if(isPlaying):
            #print("Starting.")
            playsound.playsound(path)

t = Thread(target=sound_alarm,
           args=("../assets/alarm.wav",))

def alert_value(on_off):
    global hasStarted, isPlaying
    isPlaying = on_off

    if(hasStarted == False):

        t.deamon = True
        t.start()
        hasStarted = True
