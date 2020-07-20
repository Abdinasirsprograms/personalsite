import os
import json
import collections
import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_feed/results_feed.txt')
# with open(path, 'r') as file:
#     lines = [file.readline() for line in range(7)] # get the first 7 links
#     file.close()
# print(lines)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

links = ['https://www.hiiraan.com/op4/2020/July/179053/moving_forward_while_standing_still.aspx']
class navigate_main_url:
    def __init__(self, domain, link):
        option = webdriver.firefox.options.Options()
        option.headless = True
        self.driver = webdriver.Firefox(options = option)
        self.driver.get(link)
        self.driver.implicitly_wait(5)
        self.site = self.driver.current_url
        self.top_home_site = link
        methods = ['hiiraan', 'dayniiile']
        domain = self.site.split('.')[1]
        self.method_to_call = methods.index(domain)
        self.article_data = []
        self.article_links = []
        eval(f'self.{methods[self.method_to_call]}()')

    def hiiraan(self):
        ''' assumption is article links are scrapped from rss feed '''
        get_author_js = '''
            var text = '';
            var childNodes = arguments[0].childNodes; // child nodes includes Element and Text Node
            text = childNodes[0].textContent
            return text;
        '''
        get_date_js = '''
            var text = '';
            var childNodes = arguments[0].childNodes; // child nodes includes Element and Text Node
            text = childNodes[2].textContent
            return text;
        '''
        content = self.driver.find_elements_by_xpath('//*[@id="desktopcontrol1_newsdesktop3_lblcontent"]//p[not(child::img)]')
        author_and_date = self.driver.find_element_by_xpath('//*[@id="desktopcontrol1_newsdesktop3_lblcontent"]//p[1]')
        author = self.driver.execute_script(get_author_js, author_and_date)
        date = self.driver.execute_script(get_date_js, author_and_date)
        self.article_data = [{x.tag_name:x.text} for x in content if x.text and x.text != author_and_date.text]
        self.article_data.append({'author':author})
        self.article_data.append({'date':date})
        self.tear_down()
    
        
    def dayniiile(self, link):
        ''' assumption is driver is located on an article within the webpage '''
        try:
            scraped_article = WebDriverWait(self.driver, 75).\
                        until(EC.presence_of_element_located((By.XPATH, '//article'))) 
        except TimeoutException:
            print(f'{link} has failed')
            return
        article_data = {}
        article_data['title'] = scraped_article.find_element_by_xpath('//*[contains(@class,\'td-post-title\')]//h1').text
        article_data['author'] = scraped_article.find_element_by_xpath('//div[contains(@class,\'td-post-author-name\')]//a').text
        article_data['date'] = scraped_article.find_element_by_xpath('//time').text
        article_body = scraped_article.find_elements_by_xpath('//div[contains(@class,\'td-post-content\')]/p[not(contains(concat(\' \',normalize-space(@class),\' \'),\' td-g-rec-id-content_inline \'))]')
        article_data['content'] = [[x.tag_name, x.text] for x in article_body]
        article_data['link'] = link
        if self.article_data:
            self.article_data.append([article_data])
        else: 
            self.article_data = [article_data]

    def tear_down(self):
        self.driver.close()
        self.driver.quit()

# articles = {}    
# for link in links:
#     # print(navigate_main_url(link).article_data)
#     articles[link] = navigate_main_url(link).article_data

print('*'*100)

print('file has been written to')

print('*'*100)
