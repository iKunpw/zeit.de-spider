from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import re

class Zeit(object):

    def __init__(self):
        # Start URL
        self.start_url = "https://www.zeit.de/suche/index?q=corona+pandemie+deutschland&type=article&p=1"
        self.driver = webdriver.Chrome('C:/Users/i/Desktop/Japan Supreme Bot/lib/chromedriver')
        # CSV file title
        self.start_csv = True
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(60)

    def __del__(self):
        self.driver.quit()

    def get_content(self):
        # Wait and make sure all the contents of the page can be loaded
        time.sleep(5)
        item = {}
        # Get the tab to go to the next page
        next_page = self.driver.find_element_by_xpath("//*[@id='main']/div[2]/section/div[2]/a")
        # Gets the property used to determine if it is the last page
        is_next_url = next_page.get_attribute('textContent')
        # Get a list of all li tags that store information
        li_list = self.driver.find_elements_by_xpath("//*[@id='main']/div[2]/section//article")
        # Extracting the required data
        for li in li_list:
            
            item["title"] = li.find_element_by_xpath(".//span[@class='zon-teaser-standard__title']").text

            # Save data
            self.save_csv(item)
        
        # Returns the tab for whether there is a next page and a click event for the next page,
        return next_page,is_next_url

    def save_csv(self,item):
        # Link the extracted content stored in the csv file to a csv format file
        str = ','.join([i for i in item.values()])
        with open('./zeit.csv','a',encoding='UTF-8') as f:
            if self.start_csv:
                f.write("title\n")
                self.start_csv = False
            # Writing strings to csv files
            f.write(str)
            f.write('\n')
        print("save success")

    def run(self):
        # Launch chrome and navigate to the appropriate page
        self.driver.get(self.start_url)

        while True:
            # Start extracting data and get the elements of the next page
            next_page,is_next_url = self.get_content()
            if is_next_url=='Vorherige Seite':
                break
            else:
                next_page.send_keys(Keys.ENTER)
            # Click on the next page

if __name__=='__main__':
    zeit_spider = Zeit()
    zeit_spider.run()