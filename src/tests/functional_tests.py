from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

import os
import time
import unittest


MAX_WAIT = 10


class NewVisitorTest(unittest.TestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()


        def tearDown(self):
            self.browser.quit()
            
        def browse_to_site(self):
            self.browser.get('https://abdinasirnoor.com')
            time.sleep(MAX_WAIT)
            get_http_response = self.browser.find_elements_by_tag_name('html')
            self.AssertTrue(get_http_response)
            self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
