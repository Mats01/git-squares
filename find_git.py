import datetime
import os
from pprint import pprint
from os.path import expanduser

from matplotlib import pyplot as plt
import numpy as np

def find_git_folders(path):
    git_folders = []
    for root, dirs, files in os.walk(path):
        # skip node_modules
        if '.git' in dirs and 'node_modules' not in root:
            git_folders.append(os.path.join(root, '.git'))
    return git_folders
  
  
# start form home directory
home = expanduser("~")
git_folders = find_git_folders(home + '/fer')
git_folders += find_git_folders(home + '/i1click')
git_folders += find_git_folders(home + '/rijecle')
git_folders += find_git_folders(home + '/portfolio')
pprint(git_folders)


from collections import defaultdict
import git


# dict of sting list
commit_counts = defaultdict(list)


def get_commit_counts_by_user(repo_path):
    repo = git.Repo(repo_path)
    try:
      commits = list(repo.iter_commits('HEAD'))
    except git.exc.GitCommandError:
      return
    for commit in commits:
        author = commit.author.name
        # date from unix timestamp
        timestam= commit.committed_date
        date = datetime.datetime.fromtimestamp(timestam).strftime('%Y-%m-%d')
        commit_counts[author].append(date)
    return dict(commit_counts)
  
print()
for git_folder in git_folders:
    get_commit_counts_by_user(git_folder)
    

# conbine users Mats01-fer, Mats-01, Mats01 and ''Matej Butkovic' into one
commit_counts['MatejSVE'] = commit_counts['Mats01-fer'] + commit_counts['Mats-01'] + commit_counts['Matej Butkovic'] + commit_counts['Mats01']

# count how many time each date appears in the list of 'MatejSVE'
dates = {}
    
for date in commit_counts['MatejSVE']:
    dates[date] = dates.get(date, 0) + 1
# map author to number of commits
    
pprint(dates)
pprint('total distinct commit days: %d' % len(dates.keys()))

# plot
# x axis: dates
# y axis: number of commits

# import matplotlib.pyplot as plt
# import numpy as np

# # sort dates
# dates = sorted(dates.items(), key=lambda x: x[0])

# # plot
# plt.plot([x[0] for x in dates], [x[1] for x in dates])

# # show a total of 30 dates on x axis
# plt.xticks(np.arange(0, len(dates), len(dates)/30))

# plt.xticks(rotation=90)
# plt.show()

def convert_data(data):
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

dates = sorted(dates.items(), key=lambda x: x[0])

dates = dates

import matplotlib.pyplot as plt
import numpy as np

# format date data to be used in plot
data = convert_data(dict(dates))

print(data)



# Create a new figure and axes
fig, ax = plt.subplots()

# Plot the data as an image
ax.imshow(data, cmap='Greens')

# show 40 dates along x axis
# step = len(dates) // 40
# ax.set_xticks(np.arange(0, len(dates), step))
# ax.set_xticklabels([x[0] for x in dates][::step], rotation=90)
ax.set_yticks(range(7))
ax.set_yticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

# make plot taller in y direction
ax.set_aspect(1)

# Show the plot
plt.show()
