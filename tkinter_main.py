from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, Tk 
from tkinter.ttk import Label, Style

'''Main Frame'''
root = Tk() #setup root window
root.iconbitmap('./nordicicon.ico')
root.title("Python Device Monitor Tool")
root['background']='#748587'
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
    #if else statement to test if we can login, otherwise send error and stay at login screen
    login.destroy()
    #root.deiconify() #show main window
    root.attributes('-alpha', 1)    #turn off transparency 

def exitWin():
    root.destroy()

def restartPopup():
    global logOff      
    logOff = Toplevel(root)
    logOff.attributes('-topmost', 1) #keep at the top  
    logOff.iconbitmap('./nordicicon.ico')
    logOff.title("Python Device Monitor Tool")
    logOff['background']='#abd3d9'

    #set login dimensions
    logOff_width = 250
    logOff_height = 100

    #already got screen dimensions above, now find center points
    logOff_x = int((screen_width/2) - (logOff_width/2))
    logOff_y = int((screen_height/2) - (logOff_height/2))
    logOff.geometry(f'{logOff_width}x{logOff_height}+{logOff_x}+{logOff_y}')

    logOff_label = Label(logOff, text = "Are you sure you want to log off?")
    logOff_label.config(font=('Helvatical bold', 11), background='#abd3d9')
    yes_button = Button(logOff, text="Yes", command=exitWin)
    no_button = Button(logOff, text="No", command=restartReturn)
    
    logOff.columnconfigure(0, weight=0)
    logOff.columnconfigure(1, weight=0)
    logOff.columnconfigure(2, weight=0)

    logOff_label.grid(column=0, row=0, columnspan=3, padx=15, pady=10)
    yes_button.grid(column=0, row=1, padx=2, pady=5, sticky=E)
    no_button.grid(column=2, row=1, padx=2, pady=5, sticky=W)

def restartReturn():
    logOff.destroy()

def doNothing():
    pass

start_button = Button(login, text="Enter", command=startButton, background='#41afd1',
                      padx=10, pady=5)
exit_button = Button(login, text="Exit", command=exitWin)
start_button.pack()
exit_button.place(x=20, y=240)

'''Main Screen'''
#build grid for main window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.rowconfigure(0, weight=5)
root.rowconfigure(1, weight=5)
root.rowconfigure(2, weight=5)
root.rowconfigure(3, weight=5)
root.rowconfigure(4, weight=5)
root.rowconfigure(5, weight=5)

#(0,0)select device drop down menu at top left
select_device = Button(root, text="SELECT DEVICE...", command=doNothing)
select_device.config(font=('Helvatical bold', 15), background='#abd3d9')
select_device.grid(column=0, row=0, padx=10, pady=5, sticky=EW)
'''Drop down menu, do this:
device_options = []
'''

#(0,1)below that, device information and status(?)
device_info = Label(root, text="DEVICE INFO", borderwidth=2, relief="ridge")
device_info.config(font=('Helvatical bold', 15), background='#748587')
device_info.grid(column=0, row=1, rowspan=2, padx=10, pady=5, sticky=EW)

#(0,2)below that, list subbed topics
subbed_topics = Label(root, text="Subbed\nTopics\nHere\n", borderwidth=2, relief="ridge")
subbed_topics.config(font=('Helvatical bold', 15), background='#748587')
subbed_topics.grid(column=0, row=3, rowspan=2, padx=10, pady=5, sticky=EW)

#(0,3)bottom left, log off button
acc_info = Button(root, text="Log off", command=restartPopup)
acc_info.grid(column=0, row=5, padx=5, pady=5, sticky=EW)

#(1,0)tabs(buttons) for sub/pub/msgs
sub_tab = Button(root, text="SUBSCRIBE", command=doNothing)
sub_tab.config(font=('Helvatical bold', 15), background='#abd3d9')
sub_tab.grid(column=1, row=0, padx=5, pady=5, sticky=EW)

pub_tab = Button(root, text="PUBLISH", command=doNothing)
pub_tab.config(font=('Helvatical bold', 15), background='#abd3d9')
pub_tab.grid(column=2, row=0, padx=5, pady=5, sticky=EW)

msg_tab = Button(root, text="MESSAGES", command=doNothing)
msg_tab.config(font=('Helvatical bold', 15), background='#abd3d9')
msg_tab.grid(column=3, row=0, padx=5, pady=5, sticky=EW)

nxt_tab = Button(root, text="", command=doNothing)
nxt_tab.config(font=('Helvatical bold', 15), background='#abd3d9')
nxt_tab.grid(column=4, row=0, padx=5, pady=5, sticky=EW)
nxt2_tab = Button(root, text="", command=doNothing)
nxt2_tab.config(font=('Helvatical bold', 15), background='#abd3d9')
nxt2_tab.grid(column=5, row=0, padx=5, pady=5, sticky=EW)

#(1,1)sub/pub/msgs terminal
tab_terminal = Label(root, text="Tab Activity", borderwidth=2, relief="ridge")
tab_terminal.config(font=('Helvatical bold', 20), background='#748587')
tab_terminal.grid(column=1, row=1, columnspan=5, sticky=EW)
#(1,2)user terminal
user_terminal = Label(root, text="User terminal here", borderwidth=2, relief="ridge")
user_terminal.config(font=('Helvatical bold', 20), background='#748587')
user_terminal.grid(column=1, row=3, columnspan=5, rowspan=2, sticky=EW)
#(1,3)bottom right, textbox for userinput
user_input = Label(root, text="User input goes here", borderwidth=2, relief="ridge")
user_input.config(font=('Helvatical bold', 20), background='#748587')
user_input.grid(column=1, row=5, columnspan=5, rowspan=1, sticky=EW)

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
