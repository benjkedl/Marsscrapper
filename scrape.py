
# coding: utf-8

# In[71]:


import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd


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


    # In[56]:


    browser.click_link_by_partial_text('FULL')


    # In[61]:


    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('img', class_='fancybox-image')
    src = image["src"]


    # In[63]:


    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + src
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


    # In[77]:


    mars_facts = pd.DataFrame(mars_facts)


    # In[78]:


    mars_facts_html = mars_facts.to_html()


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
    hemisphere_image_urls = dict(zip(hemi_names, hemi_urls))


    # In[92]:


    hemisphere_image_urls = dict(hemisphere_dict)

    return scrape_results = {
        'news_title': latest_title,
        'news_text': latest_description,
        'featured_img': featured_image_url,
        'mars_facts':mars_facts,
        'mars_weather': mars_weather,
        'hemispheres_dict': hemisphere_image_urls
    }

