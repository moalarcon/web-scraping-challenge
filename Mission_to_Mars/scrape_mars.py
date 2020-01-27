#!/usr/bin/env python
# coding: utf-8

# In[7]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
from selenium import webdriver
import requests as req


# In[2]:


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


# In[ ]:


def close_brower(browser):
    browser.quit()


# In[ ]:


def scrape():
## initialize and populate mars dict to hold all scraping results 
    mars = {}
    mars["news_data"] = news()
    mars["featured_image"] = images()
    mars["weather_data"] = weather()
    mars["mars_facts"] = facts()


# In[3]:


def news():
    
## initialize browser and latest_news dict
    browser = init_browser()
    latest_news = {}
    
## define url and command browser to visit and parse HTML for posts tag   
    news_url= "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('ul', class_='item_list')
    posts = []
    
## loop through results to pull out data    
    for result in results:
            # Identify and return title of post
        title = result.find('a', target_='_self').text
            # Identify and return date of post
        date = result.find('div', class_='list_date').text
            # Identify and return description to post
        description = result.find('div', class_='article_teaser_body').text
        
        print(title)
        print(date)
        print(description)
        
## add results to empty list        
        posts.append(post)
        
## add results to latest_news dictionary
        
    lastest_news['news_title']= title
    lastest_news['news_date']= date
    lastest_news['news_about']= description

## close browser
        
    close_browser(browser)
        
    return posts


# In[4]:


def images():
    browser = init_browser()
    marsimages = {}
    
    images_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('div', class_='carousel_container')
    images = []
    
    for result in results:
            # Identify and store featured image link
        image_path = result.find('a', class_='button fancybox').get(data-fancybox-href)
        featured_image_url= f'https://www.jpl.nasa.gov/{image_path}'
            # Dictionary to be inserted as a MongoDB document
        image = {
            'Featured Image URL': featured_image_url,
            }
            
        images.append(image)
    
    close_browser(browser)
        
    return images


# In[11]:


def weather():
    browser = init_browser()
    latest_weather = {}
    
    weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('div', class_='css-1dbjc4n r-my5ep6 r-qklmqi r-1adg33ll')
    mars_weather = []
    
    for result in results:
            # Identify and return title of post
        tweet = result.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
            
        print(tweet)

            # Dictionary to be inserted as a MongoDB document
        weather = {
            'Weather on Mars': tweet
            }
            
        mars_weather.append(weather)
        
    close_browser(browser)
    
    return weather


# In[5]:


def facts():
    browser = init_browser()
    mars_facts = {}
    
    facts_url= "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    print(tables)
    basic_info = tables[0]
    planet_profile = tables[1]
    
    return mars_facts

