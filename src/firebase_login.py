import pyrebase
import time
import re

from subprocess import Popen

config = {
  "apiKey": "AIzaSyD6ejYW0EFDNHgTo4Ko1Alk7U4SHTv3Jz0",
  "authDomain": "drowsiness-detector.firebaseapp.com",
  "databaseURL": "https://drowsiness-detector.firebaseio.com",
  "storageBucket": "drowsiness-detector.appspot.com"
}

IS_MANAGER = "is manager"
NOT_MANAGER = "not manager"

email = "cs189bdrowsinessdetector@gmail.com"
password = "aerospace capstone"
email2 = "davids0330@gmail.com"
password2 = "helloworld"
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
# user = auth.sign_in_with_email_and_password(email,password)
db = firebase.database()

# parses email to remove everything after the @
# this is because firebase doesn't
# allow @ to be used in the path names
# (I think, it's either this or the period)
def parseEmail(username):
    # returnString = ""
    # for x in range(0,len(username)):
    #     if (username[x] != "@" and username[x] != "."):
    #         returnString += username[x]
    return re.sub(r'\W+', '', username)

# print parseEmail("davids0330@gmail.com")

# Attempts to sign into firebase
# If successful, then it will return user data
# Otherwise returns None on failure
def signIntoFirebase(username,password):
    try:
        user = auth.sign_in_with_email_and_password(username,password)
        return user
    except Exception as e:
        return None

# Attempts to create a firebase account
# Needs a valid email to be successful
# On success, returns user data
# On failure, returns None
def createFirebaseAccount(username,password):
    try:
        user = auth.create_user_with_email_and_password(username, password)
        return user
    except Exception as e:
        return None

# createFirebaseAccount("davids0330@gmail.com","helloworld")

# General function that can create a user in the firebase database given a username and usertoken
def addUserInfo(username,user,tag,eyeRatio,mouthRatio):
    try:
        timestamp = {"First Created": time.time()}
        data = {"username": username,
                "blink frequency": 0,
                "tag":tag ,
                "current eye timestamp":0,
                "current yawn timestamp":0,
                "eye ratio":eyeRatio,
                "mouth ratio":mouthRatio,
                "timestamp":timestamp}
        db.child('users').child(parseEmail(username)).set(data,user['idToken'])
        return True
    except Exception as e:
        return False

# addUserInfo("cs189bdrowsinessdetector@gmail.com",user,NOT_MANAGER,0.1,0.2)
#
# addUserInfo("davids0330@gmail.com", user, NOT_MANAGER, 0.1,0.1)

# This is a little less reliable if other forms of authentication (ie. Github) is allowed
#addUserInfo(parseEmail("davids0330@gmail.com"), user, "is not manager", 0.1,0.1)


# timestamp = { "1": time.time(),
#               "2": time.time() }
timeStampList = [time.time(),time.time(),time.time()]

# TO DO: Starting at 0 everytime will definitely be an issue in the future
# Since all dictionary keys have to be unique
# Fix it so that it starts at reasonable value?
def createTimeStampEyes(timeStampList, start):
    timeStamp = {}
    for x in range(0,len(timeStampList)):
        timeStamp.update({"Eye "+str(x+start):timeStampList[x]})
    return timeStamp

def createTimeStampYawn(timeStampList, start):
    timeStamp = {}
    for x in range(0,len(timeStampList)):
        timeStamp.update({"Yawn "+str(x+start):timeStampList[x]})
    return timeStamp


def updateUserInfo(username,user,tag,eyeRatio,mouthRatio, blinkFrequency):
    try:
        data = {"username": username,
                "tag": tag,
                "eye ratio": eyeRatio,
                "mouth ratio": mouthRatio,
                "blink frequency": blinkFrequency}
        db.child("users").child(parseEmail(username)).update(data,user['idToken'])
        return True
    except Exception as e:
        return False

def updateEyeRatio(username,user,eyeRatio):
    try:
        data = {"eye ratio": eyeRatio}
        db.child("users").child(parseEmail(username)).update(data, user['idToken'])
        return True
    except Exception as e:
        return False

def updateMouthRatio(username,user,mouthRatio):
    try:
        data = {"mouth ratio": mouthRatio}
        db.child("users").child(parseEmail(username)).update(data, user['idToken'])
        return True
    except Exception as e:
        return False

def updateBlinkFrequency(username, user, blinkFrequency):
    try:
        data = {"blink frequency": blinkFrequency}
        db.child("users").child(parseEmail(username)).update(data, user['idToken'])
        return True
    except Exception as e:
        return False

# updateBlinkFrequency("davids0330@gmail.com", user, 118)
# updateEyeRatio("davids0330@gmail.com", user, 0.4)
# updateMouthRatio("davids0330@gmail.com", user, 0.5)

# Returns None if the username doesn't exist in the database
# Currently theres some unintentional collision if you have emails that have the same name
# Normally I wouldn't have to return None
# But there could be some permissions error so it is safer to do so anyways
def getUserData(username, user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()
    except Exception as e:
        return None

def getEyeRatio(username,user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()["eye ratio"]
    except Exception as e:
        return 0.3

def getMouthRatio(username,user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()["mouth ratio"]
    except Exception as e:
        return 0.4

# print(getEyeRatio("davids0330@gmail.com",user))
# print(getMouthRatio("davids0330@gmail.com",user))

# val = getUserData(email, user)
# print val

def getAllData(user):
    try:
        users = db.child("users").get(user['idToken'])
        return users.val()
    except Exception as e:
        raise e
        return None

def getUserBlinkFrequency(username,user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()["blink frequency"]
    except Exception as e:
        return None

def getAmountofYawns(username,user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()["current yawn timestamp"]
    except Exception as e:
        return None

def getAmountOfEyes(username,user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()["current eye timestamp"]
    except Exception as e:
        return None
# print(getAllData(user))
# print(getUserBlinkFrequency("davids0330@gmail.com",user))
# print(getAmountofYawns("davids0330@gmail.com",user))
# print(getAmountOfEyes("davids0330@gmail.com",user))

def updateEyeTimeStamps(username,user,timestampList):
    try:
        userdata = getUserData(username, user)
        userdataTimeStamps = {}
        startTimeStamp = userdata["current eye timestamp"]
        # if (startTimeStamp != 0):
        userdataTimeStamps.update(userdata["timestamp"])
        timestamp = createTimeStampEyes(timestampList,startTimeStamp)
        userdataTimeStamps.update(timestamp)
        data =  {"username":userdata["username"],
                 "eye ratio":userdata["eye ratio"],
                 "mouth ratio":userdata["mouth ratio"],
                 "blink frequency": userdata["blink frequency"],
                 "tag":userdata["tag"],
                 "current eye timestamp":startTimeStamp+len(timestampList),
                 "current yawn timestamp":userdata["current yawn timestamp"]}
        db.child("users").child(parseEmail(username)).set(data,user['idToken'])
        db.child("users").child(parseEmail(username)).child("timestamp").set(userdataTimeStamps,user['idToken'])
        return True
    except Exception as e:
        raise e
        return False

def updateYawnTimeStamps(username,user,timestampList):
    try:
        userdata = getUserData(username, user)
        userdataTimeStamps = {}
        startTimeStamp = userdata["current yawn timestamp"]
        # if (startTimeStamp != 0):
        userdataTimeStamps.update(userdata["timestamp"])
        timestamp = createTimeStampYawn(timestampList,startTimeStamp)
        userdataTimeStamps.update(timestamp)
        data =  {"username":userdata["username"],
                 "eye ratio":userdata["eye ratio"],
                 "mouth ratio":userdata["mouth ratio"],
                 "blink frequency": userdata["blink frequency"],
                 "tag":userdata["tag"],
                 "current eye timestamp":userdata["current eye timestamp"],
                 "current yawn timestamp":startTimeStamp+len(timestampList)}
        db.child("users").child(parseEmail(username)).set(data,user['idToken'])
        db.child("users").child(parseEmail(username)).child("timestamp").set(userdataTimeStamps,user['idToken'])
        return True
    except Exception as e:
        raise e
        return False

# addUserInfo(parseEmail("davids0330@gmail.com"), user, "is not manager", 0.1,0.1)
# updateEyeTimeStamps("davids0330@gmail.com",user,timeStampList)
# updateYawnTimeStamps("davids0330@gmail.com",user,timeStampList)
# addUserInfo(email,user, IS_MANAGER, 0.2,0.3)
# db.child("users").child(parseEmail(email2)).update({"current timestamp":0},user['idToken'])
# if(updateTimeStamps("davids0330@gmail.com",user,timeStampList)):
#     print "successful"
# updateEyeRatio("davids0330@gmail.com",user,0.3)

def removeUserInfo(username):
    try:
        db.child("users").child(username).remove()
        return True
    except Exception as e:
        return False

#addUserInfo("cs189bdrowsinessdetector", user, "not manager", 0.1,0.2)
#updateUserInfo("cs189bdrowsinessdetector", user, "not manager", 0.2,0.3, timestamp)
# get all data
# print(getData("davids0330@gmail.com",user))
# print(getData(email,user))
# Example:get username
#print(getData("davids0330@gmail.com",user)["username"])
#print(getData("doesn't exist"))
#removeUserInfo("cs189bdrowsinessdetector")
#updateUserInfo("davids0330@gmail.com", user, "not manager", 0.2,0.3, createTimeStamp(timeStampList))
