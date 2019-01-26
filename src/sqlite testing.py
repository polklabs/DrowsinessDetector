import Tkinter
import sqlite3
import sys
from subprocess import Popen

db = sqlite3.connect('DrowsinessDetectorDatabase')

def createUserTable(database):
    try:
        cursor = database.cursor()
        cursor.execute('''
            CREATE TABLE users(name TEXT PRIMARY KEY,
                               password TEXT)
                               ''')
    except Exception as e:
        database.rollback()
        raise e
        database.close()

def dropUserTable(database):
    try:
        cursor = database.cursor()
        cursor.execute('''
            DROP TABLE users''')
    except Exception as e:
        database.rollback()
        raise e
        database.close()

# Returns True on successful insertion of user
def addNewUser(database, user_info):
    try:
        cursor = database.cursor()
        if(isUserInDatabase(database,user_info[0])):
            print "User already exists"
            return False
        sql = ''' INSERT INTO users(name,password)
                      VALUES(?,?) '''
        cursor.execute(sql,user_info)
        return True
    except Exception as e:
        database.rollback()
        raise e
        database.close()

# Queries database for a certain user
# Returns None if the user doesn't exist
def queryUserInfo(database, username):
    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users WHERE name=?", (username,))
        user = cursor.fetchone()
        print user
    except Exception as e:
        database.rollback()
        raise e
        database.close()

# Similar to queryUserInfo()
# Instead, it returns True/False if the user exists/doesn't exist
def isUserInDatabase(database, username):
    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users WHERE name=?", (username,))
        user = cursor.fetchone()
        if user is None:
            return False
        return True
    except Exception as e:
        database.rollback()
        raise e
        database.close()

# Prints a list of all the users in the database
def selectUserNames(database):
    try:
        cursor = database.cursor()
        cursor.execute('''
            SELECT name from users''')
        for row in cursor:
            print "User name = ", row[0]
    except Exception as e:
        database.rollback()
        raise e
        database.close()

# Prints a list of all the passwords in the database
def selectUserPasswords(database):
    try:
        cursor = database.cursor()
        cursor.execute('''
            SELECT password from users''')
        for row in cursor:
            print "User password = ", row[0]
    except Exception as e:
        database.rollback()
        raise e
        database.close()

# Tests if a username/password combination is in the database
def login(database, Username, Password, message):
    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (Username,Password))
        user = cursor.fetchone()
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
        database.rollback()
        raise e
        return False

def createNewUser(db, username, password, message):
    add_user_task  = (username,password,)
    if(addNewUser(db,add_user_task)):
        message.config(text="Register Successful")
        p = Popen(["python", "start.py", username])
    else:
        message.config(text="Register Failed")

# Testing the functions

# dropUserTable(db)
# createUserTable(db)
# add_user_task = ("David Sun", "Hello World")
# addNewUser(db,add_user_task)
# selectUserIDs(db)
# selectUserNames(db)
# selectUserPasswords(db)
# user = "David Sun"
# queryUserInfo(db, user)
# queryUserInfo(db,"test")
# queryUserInfo(db,"")
# print findNextAvaliableUserID(db)

# Super basic login GUI
gui = Tkinter.Tk()
canvas = Tkinter.Canvas(gui, width=200,height=0)
canvas.pack()
a = Tkinter.Label(gui ,text="User Name")
a.pack()
b = Tkinter.Label(gui ,text="Password")
e = Tkinter.Entry(gui)
e.pack()
b.pack()
f = Tkinter.Entry(gui)
f.config(show="*")
f.pack()
c = Tkinter.Button(gui, text="LOGIN")
c.config(command=lambda:login(db,e.get(),f.get(),login_message))
c.pack()
d = Tkinter.Button(gui, text="CREATE ACCOUNT")

login_message = Tkinter.Label(gui)
d.config(command=lambda:createNewUser(db,e.get(),f.get(), login_message))
d.pack()
login_message.pack()

gui.mainloop()

db.commit()
db.close()
