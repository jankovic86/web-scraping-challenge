from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Scrape NASA Mars News.
def mars_news():
    url = 'https://redplanetscience.com/'
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    output = [news_title, news_p]
    return output


# Scrape JPL Image of the Day.
def JPL_img():
    url1 = 'https://spaceimages-mars.com/'
    browser.visit(url1)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured = soup.find('div', class_='fancybox-inner')
    featured_image = featured.find('img')['src']
    featured_image_url = url1 + featured_image
    return featured_image_url


# Mars Facts table scraping.
def mars_facts():
    url2 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url2)
    df = tables[0]
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    return html_table


# Mars Hemispheres Scrape.
def mars_hemis():
    url3 = 'https://marshemispheres.com/'
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []
    results = soup.find('div', class_='result-list')
    hemispheres = results.find_all('div', class_='item')
    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        link = hemisphere.find('a')['href']
        image_link = url3 + link
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        image_src = downloads.find('a')['href']
        image_url = url3 + image_src
        hemisphere_image_urls.append({'title': title, 'img_url': image_url})
    return hemisphere_image_urls


def scrape():
    mars_info = {}
    output = mars_news()
    mars_info["mars_title"] = output[0]
    mars_info["mars_p"] = output[1]
    mars_info["mars_image"] = JPL_img()
    mars_info["mars_facts"] = mars_facts()
    mars_info["mars_hemis"] = mars_hemis()
    return mars_info
