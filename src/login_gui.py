import Tkinter
import os
import start
import firebase_login
import calibration
from subprocess import Popen

# Designing window for registration
global success_login
success_login = 0

def register():
	global register_screen
	register_screen = Tkinter.Toplevel(main_screen)
	register_screen.title("Register")
	register_screen.geometry("300x250")
 
	global username
	global password
	global username_entry
	global password_entry
	username = Tkinter.StringVar()
	password = Tkinter.StringVar()
 
	Tkinter.Label(register_screen, text="Please enter details below", bg="blue").pack()
	Tkinter.Label(register_screen, text="").pack()
	username_lable = Tkinter.Label(register_screen, text="Email * ")
	username_lable.pack()
	username_entry = Tkinter.Entry(register_screen, textvariable=username)
	username_entry.pack()
	password_lable = Tkinter.Label(register_screen, text="Password * ")
	password_lable.pack()
	password_entry = Tkinter.Entry(register_screen, textvariable=password, show='*')
	password_entry.pack()
	Tkinter.Label(register_screen, text="").pack()
	Tkinter.Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()
 
 
# Designing window for login 
 
def login():
	global login_screen
	login_screen = Tkinter.Toplevel(main_screen)
	login_screen.title("Login")
	login_screen.geometry("300x250")
	Tkinter.Label(login_screen, text="Please enter details below to login").pack()
	Tkinter.Label(login_screen, text="").pack()
 
	global username_verify
	global password_verify
 
	username_verify = Tkinter.StringVar()
	password_verify = Tkinter.StringVar()
 
	global username_login_entry
	global password_login_entry
 
	Tkinter.Label(login_screen, text="Email * ").pack()
	username_login_entry = Tkinter.Entry(login_screen, textvariable=username_verify)
	username_login_entry.pack()
	Tkinter.Label(login_screen, text="").pack()
	Tkinter.Label(login_screen, text="Password * ").pack()
	password_login_entry = Tkinter.Entry(login_screen, textvariable=password_verify, show= '*')
	password_login_entry.pack()
	Tkinter.Label(login_screen, text="").pack()
	Tkinter.Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()

def exit_gui():
	main_screen.destroy()
	exit(1)	
	
# Implementing event on register button
 
def register_user():
 
	username_info = username.get()
	password_info = password.get()
 
	user = firebase_login.createFirebaseAccount(username_info, password_info)
	test = Tkinter.Label(register_screen, text=" ", fg="red", font=("calibri", 11))
	test.pack()
	if user == None:
		test.config(text="Password must be 6 characters or longer")
	else:
		username_entry.delete(0, Tkinter.END)
		password_entry.delete(0, Tkinter.END)
		test.config(text="Registration Success! Await Facial Calibration.", fg="green")
		test.pack()
 		calibration_values = calibration.main()
 		firebase_login.addUserInfo(username_info,user,"not manager",calibration_values[0],calibration_values[1])
 
# Implementing event on login button 
def login_verify():
	username1 = username_verify.get()
	password1 = password_verify.get()
	
	user = firebase_login.signIntoFirebase(username1, password1)
	
	
	#username_login_entry.delete(0, Tkinter.END)
	#password_login_entry.delete(0, Tkinter.END)
 
	#list_of_files = os.listdir(os.getcwd())
	#if username1 in list_of_files:
		#file1 = open(username1, "r")
		#verify = file1.read().splitlines()
	#if password1 in verify:
	if user != None:	
		login_sucess(username1, password1)
	else:
		password_not_recognised()
 
	#else:
		#user_not_found()
 
# Designing popup for login success
 
def login_sucess(username, password):
	global login_success_screen
	login_success_screen = Tkinter.Toplevel(login_screen)
	login_success_screen.title("Success")
	login_success_screen.geometry("150x100")
	Tkinter.Label(login_success_screen, text="Login Success").pack()
	Tkinter.Button(login_success_screen, text="OK", command=delete_login_success(username, password)).pack()
 
# Designing popup for login invalid password
 
def password_not_recognised():
	global password_not_recog_screen
	password_not_recog_screen = Tkinter.Toplevel(login_screen)
	password_not_recog_screen.title("Success")
	password_not_recog_screen.geometry("150x100")
	Tkinter.Label(password_not_recog_screen, text="Invalid Login ").pack()
	Tkinter.Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
	global user_not_found_screen
	user_not_found_screen = Tkinter.Toplevel(login_screen)
	user_not_found_screen.title("Success")
	user_not_found_screen.geometry("150x100")
	Tkinter.Label(user_not_found_screen, text="User Not Found").pack()
	Tkinter.Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups

def delete_login_success(username, password):
	login_success_screen.destroy()
	login_screen.destroy()
	main_screen.destroy()
	start.main(username, password)
	exit(1)
	
 
def delete_password_not_recognised():
	password_not_recog_screen.destroy()
 
def delete_user_not_found_screen():
	user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
	global main_screen
	main_screen = Tkinter.Tk()
	main_screen.geometry("300x250")
	main_screen.title("Account Login")
	Tkinter.Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
	Tkinter.Label(text="").pack()
	Tkinter.Button(text="Login", height="1", width="15", command = login).pack()
	Tkinter.Label(text="").pack()
	Tkinter.Button(text="Register", height="1", width="15", command=register).pack()
	Tkinter.Label(text="").pack()
	Tkinter.Button(text="Exit", height="1", width="15", command=exit_gui).pack()
 
	main_screen.mainloop()

while True:
	main_account_screen()