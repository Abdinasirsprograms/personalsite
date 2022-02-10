from cmath import log
from django.test import TestCase


# class websiteRequestModelEngine(TestCase):


class VisitValidLinkTest(TestCase):
    def setUp(self):
        from selenium import webdriver
        from newsreader.pull_site_data import requestWebsite
        self.re = requestWebsite('google')
        self._option = webdriver.firefox.options.Options()
        self._option.headless = True
        self._driver = webdriver.Firefox(options = self._option)
        self._driver.implicitly_wait(5)
        
    def test_selenium_started_correctly(self):
        self.site_url = 'https://google.com'
        self._driver.get(self.site_url)
        self.assertEqual(self.re._driver.title, self._driver.title)

    def test_session_id_logged_correctly(self):
        logged_session = self.re.session
        true_session = self.re._driver.session_id
        self.assertEqual(logged_session, true_session)


    def tearDown(self) -> None:
        self._driver.quit()
        self.re._driver.quit()