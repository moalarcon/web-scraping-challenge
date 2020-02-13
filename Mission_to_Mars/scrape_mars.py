#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import requests as req
import time


# ## Browser Functions

# In[2]:


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


# In[3]:


def close_browser(browser):
    browser.quit()


# ## Scraping functions

# ### Scrape Latest Mars News

# In[4]:


def scrape_news():
    try:
        ## initialize browser and latest_news dict
        browser = init_browser()
        latest_news={}


        ## define url and command browser to visit and parse HTML for posts tag   
        nasa_url= "https://mars.nasa.gov"
        news_url= "https://mars.nasa.gov/news/"
        browser.visit(news_url)
        time.sleep(1)
    
        html = browser.html
        soup = bs(html, "html.parser")
        news = soup.find_all('li', class_='slide')

        for new in news:
            ## collect title, date, description and link of post
            titles = soup.find('div', class_='content_title').text
            date = soup.find('div', class_='list_date').text
            description = soup.find('div', class_='article_teaser_body').text
            link = soup.a['href']

            ## add results to latest_news dictionary
            latest_news['news_title'] = titles
            latest_news['news_date'] = date
            latest_news['news_about'] = description
            latest_news["news_link"] = f'{nasa_url}{link}'
        print("------------PROCESSING NEWS------------")
        return latest_news
    
## close browser    
    finally:        
        close_browser(browser)


# ### JPL Maars Spaace Images - Featured Image

# In[5]:


def scrape_feat_img():
    try: 
        ##Initialize browser and empty dict; define url
        browser = init_browser()
        marsimages ={}
        image_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)
        time.sleep(1)
        ##  get tags for Featured Image carousel
        html = browser.html
        soup = bs(html, "html.parser")
        img_result = soup.find('div', class_='carousel_container')
        print("------------PROCESSING FEATURED IMG------------")
        
        ## Identify and store featured image link
        image_path = img_result.find('a', class_='button fancybox').get("data-fancybox-href")
        featured_image_url= f'https://www.jpl.nasa.gov{image_path}'
        ## Dictionary to be inserted as a MongoDB document
        marsimages["featured_img_url"] = featured_image_url

        return marsimages
    finally:
## close browser
        close_browser(browser)


# ### Latest Mars Weather from Twitter

# In[6]:


def scrape_weather():
    try:
        ##Initialize browser and empty dict; and define URL
        browser = init_browser()
        latest_weather = {}
        weather_url= "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather_url)
        time.sleep(5)
        html = browser.html
        soup = bs(html, "html.parser")
        ##define tag to parse
        print("------------PROCESSING WEATHER------------")
        tweet_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

        
        ## apend to dictionary
        latest_weather["mars_weather"] = tweet_weather
        return latest_weather
    
    finally:
        ##close browser
        close_browser(browser)


# ### Mars Facts

# In[7]:


def scrape_facts():
    mars_facts = {}
    facts_url= "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    print("------------PROCESSING FACTS------------")
    
    ## create DF of mars facts table and convert to HTML
    marsinfo_df = tables[0]
    marsinfo_df.columns = ["Mars Planet Profile" , "Mars Data"]
    marsinfo_df.set_index("Mars Planet Profile", inplace=True)
    marsfacts_html = marsinfo_df.to_html(classes = 'table table-striped')
    marsfacts_data= marsinfo_df.to_dict()
    mars_facts["mars_data_df"] = marsfacts_data
    
    return mars_facts


# ### Mars Hemispheres

# In[8]:


def scrape_hemispheres():
    try: 
        ##initiate browser; define URL and visit in browser
        browser = init_browser()
        mars_hemispheres={}
        
        hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        head_url = "https://astrogeology.usgs.gov"
        browser.visit(hemi_url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        ## define tag and parse
        hemispheres = soup.find_all('div', class_="item")
        print("------------PROCESSING HEMISPHERES------------")
        
        titles=[]
        img_urls=[]
        
        for hemi in hemispheres:
            img_title = hemi.find('h3').text
            hemi_img_url = head_url + hemi.find('a', class_="itemLink product-item")["href"]
        ## visit img url to get href for full-sized image
            browser.visit(hemi_img_url)
            url_to_full= browser.html
            soup = bs(url_to_full, "html.parser")
            full_img_url = head_url + soup.find("img", class_="wide-image")["src"]
        ## append to lists
#            titles.append(img_title)
#            img_urls.append(full_img_url)
# ## add to dict OR LIST
            mars_hemispheres["titles"]=img_title
            mars_hemispheres["links"]=full_img_url
        
        #mars_hemispheres= list(titles = titles, links = img_urls)

        return mars_hemispheres
    
    finally:
        ##close browser
        close_browser(browser)


# ## Main Scraper Function

# In[9]:


def scrape():

    try:
        browser = init_browser()
        new_news = scrape_news()
        image = scrape_feat_img()
        weather = scrape_weather()
        facts = scrape_facts()
        hemis= scrape_hemispheres()
        date = dt.datetime.now()
        print("------------PROCESSING FINAL INPUT------------")
        data = {
            "news_data": new_news,
            "featured_img_data": image,
            "weather_data": weather,
            "mars_facts": facts,
            "hemispheres_data": hemis,
            "last_modified": date
        }
        
        return data
    finally:
        close_browser(browser)


# In[10]:


if __name__ == "__main__":
    print(scrape())


# In[ ]:




