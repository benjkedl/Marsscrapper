#coding: utf-8

# In[71]:


import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

# In[42]:

def scrape():
    mars_news = requests.get('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')


    # In[43]:


    soup = bs(mars_news.text, 'html.parser')


    # In[44]:


    print(soup.prettify())


    # In[45]:


    titles = soup.find_all('div', class_='content_title')
    paragraphs = soup.find_all('div', class_='rollover_description_inner')


    # In[46]:


    latest_title = titles[0].a.text.strip()
    latest_description = paragraphs[0].text.strip()


    # In[49]:


    #jpl = requests.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    executable_path = {'executable_path': '/Users/benjk/Desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[54]:


    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(2)

    # In[56]:


    browser.find_by_id('full_image').first.click()


    # In[61]:
    
    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.find("a", class_="fancybox")["data-fancybox-href"]    


    # In[63]:


    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + image_url
    featured_image_url


    # In[64]:


    mars_twitter = requests.get('https://twitter.com/marswxreport?lang=en')
    soup = bs(mars_twitter.text, 'html.parser')


    # In[65]:


    print(soup.prettify())


    # In[66]:


    tweet_content = soup.find_all('div', class_='content')


    # In[70]:


    weather_tweets =[]
    for tweet in tweet_content:
        user_element = tweet.find('span', class_='FullNameGroup')
        user_name = user_element.strong.text.strip()
        tweet_text = tweet.find('p').text
        if (user_name == 'Mars Weather'):
            weather_tweets.append(tweet_text)
        else:
            continue

    mars_weather = weather_tweets[0]

            


    # In[73]:


    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_facts_url)

    df = mars_facts[0]
    df.columns = ["Categories", "Measurements"]
    df.set_index(["Categories"])

  
    html_table = df.to_html()
    #replace all the \n with an empty space instead
    html_table.replace('\n', '')


    # In[85]:


    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html = browser.html 
    soup = bs(html, 'html.parser')

    hemispheres = soup.find_all('div', class_='item')

    hemi_names = []
    hemi_urls = []

    for item in hemispheres:
        hemi_name = item.find('h3').text.strip()
        hemi_names.append(hemi_name)
        browser.click_link_by_partial_text(hemi_name)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find('a', text='Sample')
        img_url = img['href']
        hemi_urls.append(img_url)
        browser.visit(hemispheres_url)
     #hemisphere_image_urls = dict(zip(hemi_names, hemi_urls))


    # In[92]:


    #hemisphere_image_urls = dict(hemisphere_dict)

    scrape_results = {
        'news_title': latest_title,
        'news_text': latest_description,
        'featured_img': featured_image_url,
        'mars_facts':html_table,
        'mars_weather': mars_weather,
        'hemisphere_names': hemi_names,
        'hemisphere_urls': hemi_urls
    }
    return scrape_results

