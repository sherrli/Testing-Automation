# Testing-Automation

Automated browser tests written for UCSC Information Technology Services.
Test scripts written using Python3.7, Selenium API, chromedriver, geckodriver, and LastPass CLI.
The webdriver object opens websites and and interacts with webelements.

List of files in initial-tests
------------------------------
spreadsheet_client.py
basic_tests.py
advanced_tests.py
links_test.py
source_test.py
button_test.py
wcms_footer_header_test.py


File Descriptions
------------------------------
lastpass-login.py: a way to log in to LastPass password manager via Python to grab login credentials for tests.

client_secret.json: service account credentials for editing google spreadsheets

spreadsheet_client.py: top level calling function for all site tests
	Reads from and writes to google spreadsheet.
	Calls basic_tests and advanced_tests to determine which tests to run.
	Records the time it takes advanced tests to run.

basic_tests.py: basic validation tests to make sure all sites open
	Records the time it takes to open websites.
	Updates google spreadsheets.

advanced_tests.py: takes in a url as a parameter, and re-directs each url to a different test to be run.
	Calls links_test, source_test, button_test, wcms_footer_header_test.

links_test.py: search for all inactive links on a webpage
	Calls source_test.py to find "404 not found".
	To do: exclude reporting sites that require authentication.

source_test.py: searches a page's source code for a string

button_test.py: clicks on drop-down and search buttons on pisa class search

wcms_footer_header_test.py: searches WCMS pages for the UCSC header and footer
	Calls source_test.py to search for address and Calendars.


List of files in Login Tests
------------------------------
chain-keys.py
decode_credentials.py
encode_credentials.py
format-creds.json
lastpass-login.py
login-button-names.py
login-test.py
practice-logging.py
singlesite-login-test.py


File Descriptions
------------------------------
chain-keys.py: Practice using Selenium ActionChains to log in to a website

decode_credentials.py: Login to a site using base 64 encoded credentials

encode_credentials.py: Practice encoding credentials from a json file

format-creds.json: JSON template to storing site names, site credentials, and site urls

lastpass-login.py: Define an object with attributes that include a site's url and credentials to log in. Grabs these credentials using LastPass cli. Assumes you are already logged in to LastPass on your command line.

login-button-names.py: Names of webelements and buttons on various sites

login-test.py: Generic login test using lastpass-login.py and python's subprocess module

practice-logging.py: Practice using python's logging module

singlesite-login-test.py: Generic test to determine whether a site requires password or birthday to log in

