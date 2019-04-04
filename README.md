# Testing-Automation

Automated browser tests written for UCSC Information Technology Services.
Test scripts written using Python3, Selenium API, chromedriver, geckodriver, and LastPass CLI.
The webdriver object opens websites and and interacts with webelements.

**Author: Sherri Li** <br/>
**Email: shcli@ucsc.edu**


Main Folders
============
**headless-testing** Includes headless title tests for CHES, IDM, and LAMP, to be run remotely on a Nebula VM. These tests are used in Jenkin's Selenium pipeline. <br/>
**CHES** Includes smoke tests and functional tests for CHES sites. <br/>


Main APIs
============
**check_status.py**<br/>
	My API for making http requests on websites. Uses python requestsm module to verify the status code of a url before using webdriver to open websites.

**create_log.py**<br/>
  	My API for generating a log file at the start of each test script. Uses python logging and datetime modules to generate a log folder and file based on current system time.

**write_log.py**<br/>
  	My API for writing to the log file.

**return_credentials.py**<br/>
  	My API for interacting with LastPass through python. Contains functions to return credentials stored in LastPass. Assumes the tester has already logged into LastPass via their command line. You can save credentials in JSON format into a secure note, or as its own object.

--------------------------------------------------------------------------

Local Environment Setup
=======================
Make sure you have a Linux terminal before we begin. <br/>

----------------------------------------
1. Install Python 3 on your machine: [here](https://www.python.org/downloads/).  

To check what version of Python you have, the commands are the same across Mac and Windows.  
```
$ python3 --version (should be 3.6.5+)
$ python --version (should either be 2.7 or not exist)
```
*Note:* pip3 is an installer that comes with python3.  

For Linux/Mac, make sure that both python3 and pip3 are in your /usr/local/bin. For Windows, make sure python3 and pip3 are in your path variable. <br/>
----------------------------------------
2. Install pip3, Python's default package installer.  
**For Linux/Mac**  
```
$ echo $PATH (/usr/local/bin should appear in the PATH variable)
$ which python3
$ which pip3
```
If pip3 does not exist, run  
```
$ sudo easy_install pip3
```
Make sure these are in /usr/local/bin  
```
$ which pip3
$ sudo mv python3 /usr/local/bin
$ sudo mv pip3 /usr/local/bin
```

**For Windows**  
```
$ echo %path%
$ where pip3
$ pip3 --version
```
If pip3 was not installed on your machine, then, uninstall and reinstall python3, this time making sure to select ‘install pip’ with python3 during the installation process.  
----------------------------------------
3. Install Python's Selenium package
```
$ python3 -m pip3 install selenium
```
or
```
$ pip3 install selenium
```

----------------------------------------
4. Install additional packages
```
$ pip3 install requests
```
This package will be used to verify http response codes in various title tests.  
----------------------------------------
5. Additional Note for headless runners
Sherri advises going to see the headless-testing README to learn more about configuring the tests to run headless in the Nebula server.  
----------------------------------------
6. Install Chrome or Firefox Web Driver
Some driver executables can be found in the folder [selenium-tests/drivers](https://stash.ucsc.edu:9990/projects/WEBOPS/repos/selenium-tests/browse/drivers).  
We keep older version of the drivers there as backup, but it is recommended that you use the newest versions.  
Go to the drivers folder and extract the contents of chromedriver-v2.41-(your-OS-type) and geckodriver-v0.20.1-(your-OS-type).tar.gz into a non-git folder, then move them both to your /usr/local/bin (see below).  


You can find newest releases to [chromedriver](http://chromedriver.chromium.org/downloads) and [geckodriver](https://github.com/mozilla/geckodriver/releases).


During the time this README was written, we used chromedriver v2.41 and geckodriver v0.20.1  
*Note:* There is no chromedriver for windows 64bit, but using the 32bit version works just fine.  
*Note:* Geckodriver v0.21.0 has a tracked bug https://github.com/mozilla/geckodriver/issues/1304 so we use the previous v0.20.1.  


Now we go through moving these drivers to the right folder.  
**For Linux/Mac**  
Make sure both drivers are in your /usr/local/bin folder.  
Open terminal and run:  
```
$ sudo mv chromedriver /usr/local/bin
$ sudo mv geckodriver /usr/local/bin
```

If that doesn't work, here is a more GUI-friendly way to do it:  
Show your hidden files by typing the following command into your terminal:  
```
$ defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
```
Open your Finder  
Click MacIntosh HD  
Click 'usr' folder  
Click 'local' folder  
Click 'bin' folder  
Drag and drop chromedriver.exe and geckodriver.exe from your Downloads folder to the /usr/local/bin folder  
Hide your hidden files again by typing the following command:  
```
$ defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finder
```

**For Windows**  
Make sure the drivers are in your PATH variable.  
Search for "System Properties," go to "Advanced" tab, click "Environment Variables," click path variable, click "edit", add the location of the chromedriver and the geckodriver.  

----------------------------------------
7. Install LastPass CLI
LastPass CLI is an open-source API that can be pulled from Github. The API functions are called in our file [return_credentials.py](https://stash.ucsc.edu:9990/projects/WEBOPS/repos/selenium-tests/browse/return_credentials.py).


**For Linux/Mac**  
Check if you have Homebrew package manager installed:  
```
$ which brew
```

If you DO NOT have Homebrew, run:  
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install lastpass-cli --with-pinentry
```

Once you have Homebrew, run:  
```
$ brew update
$ brew install lastpass-cli --with-pinentry
```


**For Windows (much harder)**  
The LastPass CLI is not compatible with the Windows Terminal, so you'll need to install a Unix-like interface for your Windows.  
[Install Cygwin](https://cygwin.com/install.html ) into your C:\ directory:  
During the GUI installation process, select the following packages to include in your download:  
curl, gcc-c, gcc-g++, gcc-fortran, git, openssh, lynx, wget, rsync, python2, python3, bzip(2), tar  
Once installed, open your CygwinTerminal.lnk and run:  
```
$ lynx -source rawgit.com/transcode-open/apt-cyg/master/apt-cyg > apt-cyg
$ install apt-cyg /bin
$ apt-cyg install wget make cmake gcc-core gcc-g++ openssl-devel libcurl-devel libxml2-devel libiconv-devel cygutils-extra
$ git clone https://github.com/lastpass/lastpass-cli.git
$ cd lastpass-cli
$ make
```


Running the tests
=================
Make sure you have the Git repository cloned to your local machine.  
You can do this by changing to whichever directory you want the code to be saved in your machine, and running  
```
$ git clone ssh://git@stash.ucsc.edu:9999/webops/selenium-tests.git
```
Make sure to checkout the develop branch, where most tests are pushed to  
```
$ git checkout develop
```
Once you have the repo on your machine, open Linux terminal on Mac or Cygwin terminal on Windows, go into your local selenium-tests/ches directory, and run:  
```
$ python3 name_of_test_file.py
```

*Note:* For most people, typing
```
$ python name_of_test_file.py
```
runs name_of_test_file.py in a Python2 environment. But if your alias to Python3 is python, then go ahead and run the second one.  

We must specify python3 because tests should be run in a Python3 environment.  
This is because our tests use the functions from the subprocess module that were newly introduced in Python3.



Optional for Developers
=======================
If you will be developing new tests, install a Web Recorder.  
So far only Firefox has one that works.   
1. Open the Firefox page and go to  
https://addons.mozilla.org/en-US/firefox/
2. In the upper right search bar, type “Selenium”.
3. Find and install Katalon Recorder (Selenium IDE for FF55+)
4. Open a new Firefox browser.
5. Click the green Katalon square icon on the upper right corner of the page, to start recording web activity.
6. You can save your test cases and export them as Python2.7 files. (The selenium-python commands are backwards compatible for Python3.7 and Python2.7)


To Do
======
Figure out how to automate MFA, through LastPass CLI or Google Authenticator.
