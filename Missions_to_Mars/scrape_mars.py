#!/usr/bin/env python
# coding: utf-8

# In[74]:


from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# In[116]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[36]:


# Scrape NASA Mars News.
url = 'https://redplanetscience.com/'
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
print(soup)


# In[40]:


# results = soup.find_all('div', class_='list_text')
news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='article_teaser_body').text
print(news_title)
print(news_p)


# In[41]:


# Scrape JPL Image of the Day.
url1 = 'https://spaceimages-mars.com/'
browser.visit(url1)


# In[42]:


browser.links.find_by_partial_text('FULL IMAGE').click()


# In[50]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())


# In[73]:


featured = soup.find('div', class_='fancybox-inner')
featured_image = featured.find('img')['src']
featured_image_url = url1 + featured_image
print(featured_image_url)


# In[75]:


# Mars Facts table scraping.
url2 = 'https://galaxyfacts-mars.com/'


# In[112]:


tables = pd.read_html(url2)
tables


# In[113]:


df = tables[0]
df


# In[114]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[115]:


html_table = df.to_html()
html_table


# In[176]:


# Mars Hemispheres Scrape.
url3 = 'https://marshemispheres.com/'
browser.visit(url3)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[177]:


hemisphere_image_urls = []

results = soup.find('div', class_='result-list')
hemispheres = results.find_all('div', class_='item')

for hemisphere in hemispheres:
    title = hemisphere.find('h3').text
    link = hemisphere.find('a')['href']
    image_link = url3 + link  
    browser.visit(image_link)
    html = browser.html
    soup= BeautifulSoup(html, 'html.parser')
    downloads = soup.find('div', class_='downloads')
    image_src = downloads.find('a')['href']
    image_url = url3 + image_src
    hemisphere_image_urls.append({'title': title, 'img_url': image_url})
print(image_url)


# In[178]:


hemisphere_image_urls


# In[ ]:




