import Tkinter
import pyrebase
import time

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
user = auth.sign_in_with_email_and_password(email,password)
db = firebase.database()

# parses email to remove everything after the @
# this is because firebase doesn't
# allow @ to be used in the path names
# (I think, it's either this or the period)
def parseEmail(username):
    returnString = ""
    for x in range(0,len(username)):
        if (username[x] == "@"):
            return returnString
        returnString += username[x]

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
        data = {"username": username,
                "tag":tag ,
                "eye ratio":eyeRatio,
                "mouth ratio":mouthRatio,}
        db.child('users').child(parseEmail(username)).set(data,user['idToken'])
        return True
    except Exception as e:
        return False

# addUserInfoToken("cs189bdrowsinessdetector@gmail.com",user,NOT_MANAGER,0.1,0.2)

# This fails because @gmail.com isn't allowed as a firebase pathname
# addUserInfo("davids0330@gmail.com", user, "is not manager", 0.1,0.1)

# This works because parseEmail() will remove the @gmail.com
# This is a little less reliable if other forms of authentication (ie. Github) is allowed
#addUserInfo(parseEmail("davids0330@gmail.com"), user, "is not manager", 0.1,0.1)


# timestamp = { "1": time.time(),
#               "2": time.time() }
timeStampList = [time.time(),time.time(),time.time()]

# TO DO: Starting at 0 everytime will definitely be an issue in the future
# Since all dictionary keys have to be unique
# Fix it so that it starts at reasonable value?
def createTimeStamp(timeStampList):
    timeStamp = {}
    for x in range(0,len(timeStampList)):
        timeStamp.update({str(x):timeStampList[x]})
    return timeStamp

def updateUserInfo(username,user,tag,eyeRatio,mouthRatio, timestamp):
    try:
        data = {"username": username,
                "tag": tag,
                "eye ratio": eyeRatio,
                "mouth ratio": mouthRatio,
                "timestamp": timestamp}
        db.child("users").child(parseEmail(username)).update(data,user['idToken'])
        return True
    except Exception as e:
        return False

def updateEyeRatio(username,user,eyeRatio):
    try:
        data = {"username": username,
                "eye ratio": eyeRatio}
        db.child("users").child(parseEmail(username)).update(data, user['idToken'])
        return True
    except Exception as e:
        return False

def updateMouthRatio(username,user,mouthRatio):
    try:
        data = {"username": username,
                "mouth ratio": mouthRatio}
        db.child("users").child(parseEmail(username)).update(data, user['idToken'])
        return True
    except Exception as e:
        return False

def updateTimeStamps(username,user,timestamp):
    try:
        db.child("users").child(parseEmail(username)).child("timestamp").update(timestamp,user['idToken'])
        return True
    except Exception as e:
        return False

#updateTimeStamps("davids0330@gmail.com",user,createTimeStamp(timeStampList))
#updateEyeRatio("davids0330@gmail.com",user,0.3)


def removeUserInfo(username):
    try:
        db.child("users").child(username).remove()
        return True
    except Exception as e:
        return False

# Returns None if the username doesn't exist in the database
# Currently theres some unintentional collision if you have emails that have the same name
# Normally I wouldn't have to return None
# But there could be some permissions error so it is safer to do so anyways
def getData(username,user):
    try:
        users = db.child("users").child(parseEmail(username)).get(user['idToken'])
        return users.val()
    except Exception as e:
        return None

#addUserInfo("cs189bdrowsinessdetector", user, "not manager", 0.1,0.2)
#updateUserInfo("cs189bdrowsinessdetector", user, "not manager", 0.2,0.3, timestamp)
# get all data
# print(getData("davids0330@gmail.com",user))
# print(getData(email,user))
# Example:get username
print(getData("davids0330@gmail.com",user)["username"])
#print(getData("doesn't exist"))
#removeUserInfo("cs189bdrowsinessdetector")
#updateUserInfo("davids0330@gmail.com", user, "not manager", 0.2,0.3, createTimeStamp(timeStampList))

# Tests if a username/password combination is in the database
def login(Username, Password, message):
    try:
        user = signIntoFirebase(Username,Password)
        if user != None:
            print "success"
            message.config(text="Login Successful")
            # Here, you can probably run start.py
            p = Popen(["python", "start.py", Username])
            return True
        else:
            print "failed"
            message.config(text="Login Failed")
            return False
    except Exception as e:
        raise e
        return False

def createNewUser(username, password, message):
    add_user_task  = (username,password,)
    user = createFirebaseAccount(username, password)
    if(user != None):
        message.config(text="Register Successful")
        p = Popen(["python", "start.py", username])
    else:
        message.config(text="Register Failed")

