from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, Tk 
from tkinter.ttk import Label, Style

'''Main Frame'''
root = Tk() #setup root window
#root.geometry("1150x650+400+200")
root.iconbitmap('./nordicicon.ico')
root.title("Python Device Monitor Tool")
root['background']='#ccd9db'
#root.withdraw() #hide for now
root.attributes('-alpha', 0.9)  #make slightly transparent for now

#set window dimensions
window_width = 1150
window_height = 650

#get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#find center points
main_x = int((screen_width/2) - (window_width/2)) #center X
main_y = int((screen_height/2) - (window_height/2))   #center Y

root.geometry(f'{window_width}x{window_height}+{main_x}+{main_y}')
root.minsize(600, 300)

'''Login Frame'''
login = Toplevel(root)  #set up login window
#login.geometry("550x280+700+350")  
login.attributes('-topmost', 1) #keep at the top
login.iconbitmap('./nordicicon.ico')
login.title("nRF Cloud Account Login")
login['background']='#abd3d9'

#set login dimensions
login_width = 550
login_height = 280

#already got screen dimensions above, now find center points
login_x = int((screen_width/2) - (login_width/2))
login_y = int((screen_height/2) - (login_height/2))

login.geometry(f'{login_width}x{login_height}+{login_x}+{login_y}')
login.resizable(False, False)  #fixed size
login.overrideredirect(True)

'''Login Screen'''
myLabel1 = Label(login, text="         Welcome to the\nPython Device Monitor Tool!\n")
myLabel2 = Label(login, text = "Enter your API key: ")
myLabel1.config(font=('Helvatical bold', 20), background='#abd3d9')
myLabel2.config(font=('Helvatical bold', 15), background='#abd3d9')
myLabel1.pack(pady=15)
myLabel2.pack()

api_key = Entry(login, width=30)   #user input API key
api_key.config(font=('Helvatical bold', 14))
api_key.pack(pady=10) 
api_key.get()

def startButton(): 
    myLabel = Label(login, text="Button clicked")
    myLabel.pack() 
    login.destroy()
    #root.deiconify() #show main window
    root.attributes('-topmost', 1)
    root.attributes('-alpha', 1)    #turn off transparency 

def exitWin():
    root.destroy()

start_button = Button(login, text="Enter", command=startButton, background='#41afd1',
                      padx=10, pady=5)
exit_button = Button(login, text = "Exit", command=exitWin)
start_button.pack()
exit_button.place(x=20, y=240)

'''Main Screen'''
#build inner frame for main window
#TWO COLUMNS:
#(0,0)select device drop down menu at top left
#(0,1)below that, device information and status(?)
#(0,2)below that, list subbed topics
#(0,3)bottom left, exit button
                                        #(1,1) will be the largest vertically
#(1,0)tabs(buttons) for sub/pub/msgs
#(1,1)sub/pub/msgs 
#(1,2)terminal 
#(1,3)bottom right, textbox for userinput


root.mainloop()


'''
Use this for sub-tabs for sub/pub/msgs
login = Frame(root)
mainWin = Frame(root)

def change_to_login():
    login.pack(fill='both', expand=1)
    mainWin.pack_forget()

def change_to_mainWin():
    mainWin.pack(fill='both', expand=1)
    login.pack_forget()
'''
