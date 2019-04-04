# Contains a method to create a log folder.
# Inside the log folder is a log file.
# File names are dynamically generated, based on system time.
# Test files import this file.

import logging
import os
import datetime

# function to create log folder and log file.
# testName must be type string.
# YOU CAN CHANGE THE level==... : logging level: logging.INFO, logging.ERROR, logging.DEBUG, etc
def createLog(testName):
    timeOfTest = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-')[0:16]
    folderName = 'temp'+testName+timeOfTest
    os.makedirs('./'+folderName)
    logging.basicConfig(filename=folderName+'/'+timeOfTest + testName + 'Test.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    print("\n\u001b[33mAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    return folderName;
#^
# function to return name of the folder
