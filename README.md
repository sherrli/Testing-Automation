# Testing-Automation

Scripts written for UCSC ITS department, implement Python-Selenium automated browser testing.
The Selenium WebDriver opens and interacts with the elements on each website.

List of files
---------------------
spreadsheet_client.py
basic_tests.py
advanced_tests.py
links_test.py
source_test.py
button_test.py
wcms_footer_header_test.py


File Descriptions
---------------------
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



