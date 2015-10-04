# sensibo-python-sdk
Sensibo Python SDK

Requirements:
requests: http://www.python-requests.org/en/latest/

Uses:
ConfigParser - for use with config.ini file (static APIkey not as parameter & path to log file)
CSV - handle the log file as CSV

# The Goal
The idea with this version is to create a simple script that logs the Sensibo data to a CSV file with the API key and CSV file conveniently set outside the script using a config file.
Once the script is ready, using Task scheduler you can automate a periodic launch to log the data (you don't need the script constantly on – taking up computer resources).
With that CSV file you can later analyze the data using charts, pivots etc :)


# STEP 1 - Create your Config.INI 
  Create this file in the same directory where the script is saved
  the file should have the 3 following lines:
  
[SectionOne]
SensiboAPIkey: XXXXXXX
LogFile: C:\Users\User\Documents\GitHub\sensibo-python-sdk\Sensibo_Log.csv

# STEP 2 - Create a task to repeatedly log the data
  Assuming you want to keep track of your data over a period of time, you'll need to create a task to launch the script every XX amount of minutes and do it's thing...
  
  You can use windows task scheduler for this purpose:
  
  * Create a new task and give it a name
  * indicate in the security options that it should run whether user is logged on or not
  * Set the Trigger for daily run, recur every day, repeat every X minutes (10 - 15 should do it), duration indefinably
  * Set the action to "start a program", select the python.exe file where ever it's installed and in the arguments put the full path to the script including script file name.py
  
That should do it - test to make sure the task is running once you restart the computer (best used on a media center or some other computer that is typically on at all times).