import datetime
import os
from pprint import pprint
from os.path import expanduser

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

