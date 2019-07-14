from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    mars_dict = {}

    # Scrape news title and paragraph text
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Add news title and paragraph text to mars dictionary
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    # Scrape featured image url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)  

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    end_url = soup.find('footer').find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + end_url

    # Add featured image url to mars dictionary
    mars_dict['feature_img'] = featured_image_url

    # Scrape mars weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_='tweet-text').text

    # Add weather to mars dictionary
    mars_dict['weather'] = mars_weather

    # Scrape mars data table
    url = 'https://space-facts.com/mars/'

    table = pd.read_html(url)[1]
    mars_data_table = table.rename(columns={0:'Description', 1:'Values'}).set_index('Description')
    mars_data_table = str(mars_data_table.to_html())

    # Add marsmars dictionary
    mars_dict['mars_data_table'] = mars_data_table



    # Scrape hemisphere images 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    links_to_click = ['Valles Marineris Hemisphere Enhanced', 'Cerberus Hemisphere Enhanced', 
                      'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced']

    hemisphere_image_urls = []

    for link in links_to_click:
        try:
            browser.click_link_by_partial_text(link)
            
        except:
            browser.click_link_by_partial_text('2')
            browser.click_link_by_partial_text(link)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('h2', class_='title').text
        title = title.rsplit(' ', 1)[0]

        src = soup.find('img', class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov' + src

        # Dictionary to be inserted into list
        img = {
            'title': title,
            'img_url': img_url
        }

        hemisphere_image_urls.append(img)
    
    # Add hemisphere images to mars dictionary
    mars_dict['hemisphere_imgs'] = hemisphere_image_urls

    return mars_dict


