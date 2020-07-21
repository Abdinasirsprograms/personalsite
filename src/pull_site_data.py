#!/usr/bin/env python
import os
import datetime
import collections
import django
from selenium import webdriver
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personalsite.settings")
django.setup()
from django.db import models 
from newsreader.models import Article_site, Article_links


class Site_data:
    def __init__(self):
        option = webdriver.firefox.options.Options()
        option.headless = True
        self.driver = webdriver.Firefox(options = option)
        self.driver.implicitly_wait(5)
        try:
            self.html_sites = Article_site.objects.filter(website_type__exact='HTML')
            self.xml_sites = Article_site.objects.filter(website_type__exact='XML')
            self.get_xml_site_links()
            self.get_html_site_links()
            self.tear_down()
        except Exception as e:
            print('Article site fetch failed with the following exception:', e)
            self.tear_down()

    def get_xml_site_links(self):
        if self.xml_sites:
            for site in self.xml_sites:    
                results = Walk_through_XML(site.link_to_site, site.language, self.driver).results
                '''
                list of lists that contain the following dictionary keys - 
                'title', 'link', 'description' and  'pubdate'
                '''
                if results:
                    print('^'*25, f'XML Articles foundfor {site.domain}', '^'*25)
                    for i in range(len(results)):
                        article_exists = Article_links.objects.filter(site=site).filter(article_link=results[i]['link'])
                        if article_exists:
                            print('x'*25, 'Object already in DB', 'x'*25)
                            continue
                        article_input = Article_links()
                        print('*'*25, 'Inputing object to DB', '*'*25)
                        article_input.title =results[i]['title']
                        article_input.article_link = results[i]['link']
                        article_input.description = results[i]['description']
                        time_formatted = results[i]['pubdate'].replace('EDT', '').replace('EST', '') #ONLY UTC and GMT are avalible in strptime
                        try:
                            time = datetime.datetime.strptime(time_formatted, "%A, %d %b %Y %H:%M ")   
                        except:
                            time = datetime.datetime.strptime(time_formatted, "%a, %d %b %Y %H:%M ")   
                        article_input.date_posted = time
                        article_input.site = site
                        try:
                            article_input.save()
                        except Exception as e: 
                            print(e)
                        print('*'*25, 'EOF', '*'*25)
                else:
                    print('x'*25, 'No articles retrieved', 'x'*25)
    
    def get_html_site_links(self):
        if self.html_sites:
            for site in self.html_sites:
                results = Walk_through_HTML(site.link_to_site, site.language, self.driver).results
                '''
                List that contains the dictionaries with the following keys -
                link and title 
                '''
                if results:
                    print('^'*25, f'HTML Articles found for {site.domain}', '^'*25)
                    for i in range(len(results)):
                        article_exists = Article_links.objects.filter(site=site).filter(article_link=results[i]['link'])
                        if article_exists:
                            print('x'*25, 'Object already in DB', 'x'*25)
                            continue
                        article_input = Article_links()
                        print('*'*25, 'Inputing object to DB', '*'*25)
                        article_input.title = results[i]['title']
                        article_input.article_link = results[i]['link'] 
                        article_input.site = site
                        try:
                            article_input.save()
                        except Exception as e: 
                            print(e)
                        print('*'*25, 'EOF', '*'*25)
    def tear_down(self):
        self.driver.close()
        self.driver.quit()

class Walk_through_XML:
    def __init__(self, link, lang, driver):
        self.driver = driver
        self.driver.get(link)
        site_is_xml = 'xml' in self.driver.current_url
        if site_is_xml == False: raise Exception('XML Site not passed, please check URL')
        self.top_level_elem = self.driver.find_element_by_xpath('/*').tag_name
        if self.top_level_elem == ('html' or 'HTML'): raise Exception('XML Site not passed, please check URL')
        self.root_elem = self.driver.find_element_by_xpath('/*/child::*').tag_name
        self.parents = []
        self.search_for_tags = ['date','title','link','desc']
        self.exclude = ['image', 'copyright', 'language']
        self.results = self.hiiraan()

    def hiiraan(self):
        self.parents = self.driver.find_elements_by_xpath(f'//{self.root_elem}/*') 
        count_list = [x.tag_name for x in self.parents if x.tag_name not in self.exclude] 
        count_dict = collections.Counter(count_list) # O(n) collections to be depracted in py v3.10
            
        for parent in count_dict.keys(): 
            results = []
            if count_dict[parent] > 1:
                for i in range(count_dict[parent]+1): 
                    ele = self.driver.find_elements_by_xpath(f'//{parent}[{i}]/*') 
                    if ele:
                            article = {}
                            for child in ele:          
                                key = child.tag_name
                                value = child.get_attribute("textContent") if not child.text else child.text
                                article[key] = value
                            results.append(article)
        return results       

class Walk_through_HTML:
    def __init__(self, link, language, driver):
        self.driver = driver
        self.driver.get(link)
        self.site = self.driver.current_url
        self.top_home_site = link
        self.top_level_elem = driver.find_element_by_xpath('/*').tag_name
        if self.top_level_elem != ('html' or 'HTML'): raise Exception('HTML Site not passed, please check URL')
        self.root_elem = driver.find_element_by_xpath('/*/child::*').tag_name
        self.results = self.dayniiile()
    
    def dayniiile(self):
        ''' assumption, article links need to be scraped from homepage first '''
        links = self.driver.find_elements_by_xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' td-big-grid-post ')]//a")
        article_links = []
        for link in links:
            if (link.get_attribute('href') != self.site and self.top_home_site) and (link.get_attribute('href') not in article_links): 
                if (link.get_attribute('href') != 'https://www.dayniiile.com/author/admin/') and (link.get_attribute('href') != 'https://www.dayniiile.com/author/somali/'):
                    title = link.get_attribute('title')
                    article_link = link.get_attribute('href')
                    article_links.append({'title':title, 'link':article_link})  
        return article_links

if __name__ == "__main__":    
    print('*'*100)

    Site_data()

    print('*'*100)



