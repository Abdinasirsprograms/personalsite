import os
import datetime
import collections
import django
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personalsite.settings")
django.setup()
from django.db import models 
from newsreader.models import Article_site, Article_links, Article_content

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Article_data:
    def __init__(self):
        try:
            self.site_links = Article_links.objects.filter(scrapped__exact=False).order_by('site')
            self.start_up()
            self.pull_article_data()
            self.tear_down()
        except Exception as e:
            print('Article link fetch failed with the following exception:', e)
            self.tear_down()
    
    def start_up(self):
        option = webdriver.firefox.options.Options()
        option.headless = True
        self.driver = webdriver.Firefox(options = option)
        self.driver.implicitly_wait(5)

    def pull_article_data(self):
        if self.site_links:
            counter = 0
            for link in self.site_links:
                current_date = datetime.date.today()
                if link.date_posted:
                    time_delta = current_date - link.date_posted
                    if time_delta.days <= 7:
                        counter += 1
                        data = navigate_main_url(link, self.driver).article_data
                        if type(data) == datetime.datetime:
                            link.date_posted = data
                            link.scrapped = True
                            link.save()
                        else:
                            article_input = Article_content()
                            if link.site.domain == 'hiiraan.com':
                                article_input.title = link.title
                                article_input.article_content = data['p']
                                article_input.author = link.site.domain if not data['author'] else data['author']
                                article_input.date_posted = link.date_posted if link.date_posted else data['date']
                                article_input.link_to_content = link
                                link.scrapped = True
                                link.author = link.site.domain if not data['author'] else data['author']
                                link.save()
                                article_input.save()
                            if link.site.domain == 'dayniiile.com':
                                article_input.title = link.title
                                article_input.article_content = data['content']
                                article_input.author = link.site.domain if not data['author'] else data['author']
                                article_input.date_posted = link.date_posted if link.date_posted else data['date']
                                article_input.link_to_content = link
                                link.author = link.site.domain if not data['author'] else data['author']
                                link.scrapped = True
                                link.save()
                                article_input.save()
                    else:       
                        link.scrapped = True
                        link.save()
                        continue
                else:
                    counter += 1
                    data = navigate_main_url(link, self.driver).article_data
                    if type(data) == datetime.datetime:
                        link.date_posted = data
                        link.author = link.author if link.author else link.site.domain
                        link.scrapped = True
                        link.save()
                    else:
                        print(data)
                if counter % 10 == 0:
                    self.tear_down()
                    time.sleep(5)
                    self.start_up()

    def tear_down(self):
        self.driver.close()
        self.driver.quit()

class navigate_main_url:
    def __init__(self, site_link, driver):
        self.driver = driver
        time.sleep(2)
        self.driver.get(site_link.article_link)
        self.site = self.driver.current_url
        self.top_home_site = site_link.article_link
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
            try{
                text = childNodes[2].textContent;
            }
            catch(e){
                text = undefined;
            }
            finally{
                if(text !== undefined){
                    return text;
                } else {
                    return ' '
                };
            };
        '''
        try:
            content = self.driver.find_elements_by_xpath('//*[@id="desktopcontrol1_newsdesktop3_lblcontent"]//p[not(child::img)]')
            content_somali = ''
            if not content:
                raise Exception('Navigating somali site')
        except Exception as e:
            content = ''
            content_somali = self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[4][not(contains(concat(\' \',normalize-space(@class),\' \'),\' inline-ad \'))]')
        try:
            if content:
                author_and_date = self.driver.find_element_by_xpath('//*[@id="desktopcontrol1_newsdesktop3_lblcontent"]//p[1]')
                author_and_date_text = author_and_date.text
                author = self.driver.execute_script(get_author_js, author_and_date)
                date = self.driver.execute_script(get_date_js, author_and_date)
            else:
                raise Exception('Somali site doesn\'t have authors')
        except Exception as e:
            author_and_date_text = ''
            try:
                author = self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[contains(@align,\'justify\')][last()]').text
                author = author[0: author.index(',')- 1] + '' 
                author = 'by ' + author
                if len(author) > 100:
                    author = ''
            except:
                author = ''
            date = ''
            print(f'error processing location for {self.top_home_site}: {e}')
        self.article_data = {'p':''}
        if content_somali:
            self.article_data['p'] += ' ' + content_somali.text if self.article_data['p'] else '' + content_somali.text # add space after elements
        elif content:
            for item in content:
                if item.text and item.text != author_and_date_text:
                    if item.tag_name == 'p':
                        self.article_data['p'] += '' + item.text
        self.article_data['author'] = author
        self.article_data['date'] = date
    
        
    def dayniiile(self):
        ''' assumption is driver is located on an article within the webpage '''
        try:
            scraped_article = WebDriverWait(self.driver, 75).\
                        until(EC.presence_of_element_located((By.XPATH, '//article'))) 
        except TimeoutException:
            print(f'{self.top_home_site} has failed')
            return
        article_data = {}
        article_data['title'] = scraped_article.find_element_by_xpath('//*[contains(@class,\'td-post-title\')]//h1').text
        author = scraped_article.find_element_by_xpath('//div[contains(@class,\'td-post-author-name\')]//a').text
        if author == 'admin':
            article_data['author'] = self.top_home_site
        else:
            article_data['author'] = 'by ' + author
        posted_date = scraped_article.find_element_by_xpath('//time').text
        try:
            time_posted = datetime.datetime.strptime(posted_date, '%B %d, %Y') 
        except:
            time_posted = posted_date
            print(posted_date)
        article_data['date'] = time_posted
        article_body = scraped_article.find_elements_by_xpath('//div[contains(@class,\'td-post-content\')]/p[not(contains(concat(\' \',normalize-space(@class),\' \'),\' td-g-rec-id-content_inline \'))]')
        article_data['content'] = ''
        for content in article_body:
            article_data['content'] += ' ' + content.text if article_data['content'] else '' + content.text
        article_data['link'] = self.top_home_site
        if article_data['content']:
            current_time = datetime.datetime.now()
            time_delta = current_time - time_posted
            if time_delta.days < 7:
                self.article_data = article_data
            else:
                self.artticle_data = time_posted
        else:             
            self.article_data = time_posted


if __name__ == "__main__":        
    print('*'*100)
    print('\t\tExecuting Pull Article Data\n')
    Article_data()

    print('*'*100)
