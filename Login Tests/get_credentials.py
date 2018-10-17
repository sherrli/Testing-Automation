# Require Python version 3.5+
# Require LastPass CLI

import base64
import subprocess
import sys
from io import StringIO

class ReturnSite(object):
    # the class makes it easier to return multiple values
    def __init__(self, user, pw, url, notes):
        self.user = user
        self.pw = pw
        self.url = url
        self.notes = notes

def get_value(username, siteName):
    subprocess.call(['lpass', 'login', username])
    output1 = subprocess.Popen(['lpass', 'show', siteName, '--username'], stdout=subprocess.PIPE)
    user, err = output1.communicate()
    output2 = subprocess.Popen(['lpass', 'show', siteName, '--password'], stdout=subprocess.PIPE)
    pw, err = output2.communicate()
    output3 = subprocess.Popen(['lpass', 'show', siteName, '--url'], stdout=subprocess.PIPE)
    url, err = output3.communicate()
    output4 = subprocess.Popen(['lpass', 'show', siteName, '--notes'], stdout=subprocess.PIPE)
    notes, err = output4.communicate()
    return ReturnSite(user.decode(), pw.decode(), url.decode(), notes.decode())


def get_all_values(username, siteList):
    subprocess.call(['lpass', 'login', username])
    output = subprocess.Popen(['lpass', 'show', siteList, '--notes'], stdout=subprocess.PIPE)
    out, err = output.communicate()
    #print("here is the output:\n")
    #print(out)
    #out = out.replace(b'\n',b'')
    #out = out.replace(b'\t',b'')
    return (out.decode())
