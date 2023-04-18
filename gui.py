import os
from os.path import expanduser
from tkinter import *


def find_git_folders(path):
    git_folders = []
    for root, dirs, files in os.walk(path):
        # skip node_modules
        if '.git' in dirs and 'node_modules' not in root:
            git_folders.append(os.path.join(root, '.git'))
    return git_folders
  
  
# start form home directory
home = expanduser("~")


home_folders = os.listdir(home)
# exclude hidden folders
home_folders = [folder for folder in home_folders if not folder.startswith('.')]
# sort folders
home_folders.sort()





def submit():
    
    
    
    selected = []
    for i in range(len(var_list)):
        if var_list[i].get() == 1:
            selected.append(options[i])
    
    
    git_folders = []
    
    for i in selected:
        git_folders += find_git_folders(home + '/' + i)
        
    
        
    usernames = entry.get().split(",")
    
    print("Usernames:", usernames)
    
    root.destroy()
        
    


var_list = []
root = Tk()
options = home_folders


root.title("Git activity")

frame = Frame(root)
frame.pack(fill=BOTH, expand=1)

canvas = Canvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)


label = Label(frame, text="Enter comma-separated list of your usernames:")
label.pack()

entry = Entry(frame)
entry.pack()



submit_button = Button(frame, text="Submit", command=submit)
submit_button.pack()

scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")



for option in options:
    var = IntVar()
    c = Checkbutton(inner_frame, text=option, variable=var, anchor="w")
    c.pack(fill=X)
    var_list.append(var)









def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


canvas.bind("<Configure>", on_configure)
root.mainloop()