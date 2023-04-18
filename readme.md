# Git Commit Frequency Graph

Ever had this problem: you constantly work on some code but you have loads of git accounts on different services so your GitHub Contributions graph looks sad and empty? 

**Here is the solution you've been looking for!** 
Just run this little Python app and it will find every git folder on your machine and combine them into a Contribution graph greener than a golf course 😎

This Python app scrapes your disk for git folders and generates a green square graph of your commit frequency.

## Features
- Allows users to select which root folders to look through
- Users can input their usernames
- Generates a green square graph of commit frequency

## Setup
1. Create a Python virtual environment: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`

## Usage
1. Run the app: `python3 gui.py`
2. Select the root folders you want to search for git folders
3. Input your username
4. View your commit frequency graph

Enjoy!