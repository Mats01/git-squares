import os
from os.path import expanduser
from tkinter import *
from collections import defaultdict
import git
import datetime
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np


commit_counts = defaultdict(list)


def find_git_folders(path):
    git_folders = []
    for root, dirs, files in os.walk(path):
        # skip node_modules
        if '.git' in dirs and 'node_modules' not in root:
            git_folders.append(os.path.join(root, '.git'))
    return git_folders
  
def get_commit_counts_by_user(repo_path, authors):
    repo = git.Repo(repo_path)
    try:
      commits = list(repo.iter_commits('HEAD'))
    except git.exc.GitCommandError:
      return
    for commit in commits:
        author = commit.author.name
        if(author not in authors):
          continue
        # date from unix timestamp
        timestam= commit.committed_date
        date = datetime.datetime.fromtimestamp(timestam).strftime('%Y-%m-%d')
        commit_counts[author].append(date)
  


def plot_data(dates):

    # x axis: dates
    # y axis: number of commits

    import matplotlib.pyplot as plt
    import numpy as np

    # sort dates
    dates = sorted(dates.items(), key=lambda x: x[0])

    # plot
    plt.plot([x[0] for x in dates], [x[1] for x in dates])

    # show a total of 30 dates on x axis
    plt.xticks(np.arange(0, len(dates), len(dates)/30))

    plt.xticks(rotation=90)
    plt.show()
    
    
def convert_data(data):
  
    # limit all values above 10 to 10 to get a more readable plot
    data = {k: min(v, 10) for k, v in data.items()}
    # Get the start and end dates from the data
    start_date = datetime.datetime.strptime(min(data.keys()), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(max(data.keys()), '%Y-%m-%d')

    # Calculate the number of weeks between the start and end dates
    num_weeks = (end_date - start_date).days // 7 + 1

    # Create an array to hold the converted data
    converted_data = np.zeros((7, num_weeks), dtype=int)

    # Fill in the converted data
    for date_str, count in data.items():
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        week = (date - start_date).days // 7
        day = date.weekday()
        converted_data[day, week] = count

    return converted_data
  
  
def plot_squares(dates):
  data = convert_data(dict(dates))

  print(data)



  # Create a new figure and axes
  fig, ax = plt.subplots()

  # Plot the data as an image
  ax.imshow(data, cmap='Greens')


  start_date = datetime.datetime.strptime(min(dates.keys()), '%Y-%m-%d')
  end_date = datetime.datetime.strptime(max(dates.keys()), '%Y-%m-%d')
  # Calculate the number of weeks between the start and end dates
  weeks = (end_date - start_date).days // 7 + 1
  
  # show a few dates along x axis starting from the first date and ending with the last date
  # up to 40 dates
  # if there are less than 40 dates, show all of them
  ax.set_xticks(range(weeks)[::weeks//(40 if weeks > 40 else weeks)])
  ## print labels YYYY-MM-DD
  # formaat date to string
  ax.set_xticklabels([(start_date + datetime.timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(weeks)][::weeks//(40 if weeks > 40 else weeks)], rotation=90)
  
  ax.set_yticks(range(7))
  ax.set_yticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

  # make plot taller in y direction
  ax.set_aspect(1)

  # Show the plot
  plt.show()
  
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
    
    
    root.destroy()

    print("Usernames:", usernames)
    
    for git_folder in git_folders:
        get_commit_counts_by_user(git_folder, usernames)
        
    # conbine users Mats01-fer, Mats-01, Mats01 and ''Matej Butkovic' into one
    commit_counts['MatejSVE'] = commit_counts['Mats01-fer'] + commit_counts['Mats-01'] + commit_counts['Matej Butkovic'] + commit_counts['Mats01']

    # count how many time each date appears in the list of 'MatejSVE'
    dates = {}
        
    for date in commit_counts['MatejSVE']:
        dates[date] = dates.get(date, 0) + 1
    # map author to number of commits
        
    pprint('total distinct commit days: %d' % len(dates.keys()))
    plot_squares(dates)
    
    
        
    


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