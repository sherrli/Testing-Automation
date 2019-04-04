Name: README.md for CHES automated tests  
Author: Sherri Li
__Note__: See [parent directory readme](https://stash.ucsc.edu:9990/projects/WEBOPS/repos/selenium-tests/browse/readme.md) for environment setup.

Test Files
==========
adms_test.py<br/>
	Makes sure that the admissions statistics data populates the adms dev site https://admstats.sa-dev.ucsc.edu/. The test even screenshots of the page!

ches_sa_new_test_titles.py<br/>
	A title test for the ches-sa-new sites listed in the file sites-sa-new.json

ches_dev_new_test_titles.py<br/>
	A title test for the ches-dev-new sites listed in the file sites-dev-new.json

ches_dev_test_titles.py<br/>
	A title test for the ches-dev sites listed in the file sites-dev.json

ches_lpass_login_test.py<br/>
	An automated login test for dev, dev-new, and prod sites in the LastPass file ches-dev-pw-creds.json. Pulls login credentials from LastPass using Python's subprocess module along with the LastPass CLI. Imports the file return_credentials.py in the selenium-tests parent directory.

ches_prod_test_titles.py<br/>
	A title test for the ches prod sites listed in the file sites-prod.json

ches_stage_test_titles.py<br/>
	A title test for the ches stage sites listed in the file sites-stage.json

ches-buttons.py<br/>
	Stores the names of buttons and web elements to ches dev sites in a dictionary format. Exists to help you locate elements, this file is never directly used in anything. Feel free to delete it.

ches-stage-url-test.py<br/>
	Uses Python's urllib3 package to check the HTTP status codes of ches stage sites.

cmd_check_stage.py<br/>
	Template for mapping site information from a JSON to a python dictionary.

fixit_ticket_test.py<br/>
	Ticket creation and ticket status check for https://fixit.sa-dev.ucsc.edu/ and https://fixit.sa-dev-new.ucsc.edu/.  Pulls login credentials from LastPass by importing return_credentials.py from parent directory selenium-tests.

old_ches_title_test.py<br/>
	An outdated title test with proxy connections to the Remote Selenium server. Written by the legendary Andre himself.

old_ches_login_test.py<br/>
	Outdated login test for ches-dev sites by decoding base64-encoded credentials in the deleted files login-pw.txt and login-bd.txt

old_vault_login.py<br/>
	Outdated LastPass command-line login using the LastPass python module. We now use LastPass CLI on github, to access site credentials.

otss_test.py<br/>
	Outdated login test to https://eop.sa-stage.ucsc.edu/OTSS/lcadmin/



Data Files
==========
sites-dev.json<br/>
	Dictionary of ches-dev sites and titles for ches_dev_test_titles.py

sites-dev-new.json<br/>
	Dictionary of ches-dev-new sites and titles for ches_dev_new_test_titles.py

sites-sa-new.json<br/>
	Dictionary of ches-sa-new sites and titles for ches_sa_new_test_titles.py

sites-prod.json<br/>
	Dictionary of ches-prod sites and titles for ches_prod_test_titles.py

sites-stage.json<br/>
	Dictionary of ches-stage sites and titles for ches_stage_test_titles.py  
