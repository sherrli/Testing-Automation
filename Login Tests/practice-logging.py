import logging
import lastpass-login
#TODO: put logging command into a class so that each test can generate its own log file

logging.basicConfig(filename='test-results.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
# see LogRecord attributes on PyDocs

class Test:
    """A sample test class"""
    
    def __init__(self, sitename):
        self.sitename = sitename
        logging.info('Testing started for: {}'.format(self.sitename))
        
    @property
    def result(self):
        # if test passes:
        logging.info('Test passed')
        # else if test fails:
        logging.info('Test failed')
        # return '{} test passed'.format(self.sitename)

test_1 = Test('btc') # Bay Tree Conference
test_2 = Test('otss') # Online Tutor Signup System
