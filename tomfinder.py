#!/usr/bin/python3
"""
How I obtained test.log: 

`docker run -it --rm tomcat:8.0`

Then copy the stdout to test.log so that I could verify what type of tomcat logformat will be used here
"""


"""
Also I'm bit confused of the use case for this question.


The question askes: 

"....searches a tomcat log (let’s call it test.log) for the message “test message”. 
If it finds a matching record from the last 45 minutes, it should do nothing; 
however, if the message is not found, or it is more than 45 minutes old, it should try to restart the tomcat process gracefully.
..."

My understanding is as following: 

```
if "test message" and time < 45 min:
    do nothing
if not "test message" or found "test message" but > 45 min: 
    restart tomcat

====> In other words, in time 10 we found "test message" we do nothing, but that log message will stick around, eventually
it will be found and over 45 minutes, and we will need to restart tomcat from then on, regardless of any other conditions.

"""

import argparse
import os
import re
import subprocess
import time
from datetime import datetime, timedelta

script_execution_time = datetime.now()
FMT = '%d-%b-%Y %H:%M:%S.%f'
find_all_kill_all = "kill $(ps aux | grep [c]atalina.startup.Bootstrap | awk '{print $2}')"

def findMatchingLines(file, string):

    with open(file, 'r') as f:
        line = f.readline()
        for line in f:
            if line.strip():
                if (re.search(string, line)):
                    list = line.split(' ')
                    date = list[0]
                    time = list[1]
                    content = list[2:]
                    dt = " ".join(list[:2])
                    delta = datetime.strptime(dt, FMT) - datetime.now()
                    delta_minute = int(delta.total_seconds() / 60)
                    if -45 <= delta_minute <= 0:
                        print("delta_minute = ", delta_minute)
                        print(line)
                        print("should do nothing....")
                if not (re.search(string, line)) or delta_minute <= -45:
                    commence_start_stop_process()
                    break

def commence_start_stop_process():
    
    try:
        print("===> Stopping Tomcat....")
        p = subprocess.Popen(tomcat_stop, shell=True).wait(timeout=20)
    except TimeoutError:
        print("===> Failed to stop Tomcat after 20 seconds...")
        print("===> Find and kill all tomcat processes...")
        os.system(find_all_kill_all)
    finally:
        print("===> Starting up Tomcat....")
        subprocess.call(tomcat_start)


if __name__ == '__main__':
    try:
        catalina_home = os.environ['CATALINA_HOME']
        tomcat_stop = catalina_home + '/bin/shutdown.sh'
        tomcat_start = catalina_home + '/bin/startup.sh'
    except KeyError:
        print("You do not have Tomcat installed properly")
        exit(-1)
    
    parser = argparse.ArgumentParser(description='file path for the log file')
    parser.add_argument('-f', required=True, type=str, help='file path for the log file')
    parser.add_argument('-s', required=True, type=str, help='string you want to search for')

    args = parser.parse_args()
    findMatchingLines(args.f, args.s)