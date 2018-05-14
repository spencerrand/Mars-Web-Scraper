
# coding: utf-8

# In[25]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import urllib.request


def scrape():

    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/'

    # Path for Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}

    # Launch Chrome browser
    browser = Browser('chrome', **executable_path, headless=False)

    # Go to url for news about mars
    browser.visit(mars_news_url)

    # Get HTML from browser
    html = browser.html

    # Turn HTML into BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the parent item for all news items
    results = soup.find_all('li', class_='slide')

    # Get the header and paragraph text from the first news item
    news_paragraph = results[0].find('div', class_='article_teaser_body').text
    news_header = results[0].find('h3').text

    # Close and exit browser session
    browser.quit()

    # URL for featured image of Mars
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Retrieve page with the requests module
    response = requests.get(jpl_image_url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Retrieve the item that has the url for featured image
    results = soup.find_all('a', class_='button fancybox')

    # Get url for featured image
    featured_image_url = 'https://www.jpl.nasa.gov'+results[0]['data-fancybox-href']

    # Save image
    urllib.request.urlretrieve(featured_image_url, 'featured-image.jpg')

    # URL for Mars weather twitter account
    mars_twitter_url = 'https://twitter.com/marswxreport'

    # Retrieve page with the requests module
    response = requests.get(mars_twitter_url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Retrieve parent item of tweets
    results = soup.find_all('div', class_='js-tweet-text-container')

    # Store first tweet
    mars_weather = results[0].find('p').text

    # url for Mars facts
    mars_facts_url = "https://space-facts.com/mars"

    # Read table from url using pandas
    tables = pd.read_html(mars_facts_url)

    # Convert table to HTML
    mars_table_html = tables[0].to_html()

    # Remove \n from string
    mars_table_html = mars_table_html.replace('\n', '')

    # url to search for Mars hemisphere images
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with requests module
    response = requests.get(mars_hemi_url)

    # Convert to BeautifulSoup object and parse with lxml
    soup = BeautifulSoup(response.text, 'lxml')

    # Retrieve parent item that has the search results
    results = soup.find_all('div', class_='item')

    # Create empty list to store image titles and urls
    hemispheres_image_urls = []

    # Loop through the search results
    for result in results:

        # Create an empty dictionary to store image title and url
        img_dict = {}

        # Find the text from the h3 tag
        title = result.find('h3').text

        # Strip out unwanted words
        title = title.replace(' Enhanced', '')

        # Add title to dictionary
        img_dict['title'] = title
    
        # Find the link to the image
        link = result.find('a')['href']

        # Add in https... to link to create full url
        full_link = 'https://astrogeology.usgs.gov' + link

        # Retrieve page using requests module
        img_response = requests.get(full_link)

        # Convert to BeautifulSoup object and parse using lxml
        img_soup = BeautifulSoup(img_response.text, 'lxml')
    
        # Find all div items that has the url information
        img_results = img_soup.find_all('div', class_='downloads')

        # Find url in first result
        img_url = img_results[0].find_all('a')[0]['href']

        # Add url to dictionary
        img_dict['img_url'] = img_url
    
        # Append dictionary to list
        hemispheres_image_urls.append(img_dict)

        # Replace spaces with dashes and add JPG as file name extension
        img_file_name = img_dict['title'].replace(' ','-')+'.jpg'
    
        # Save image
        urllib.request.urlretrieve(img_dict['img_url'], img_file_name)

    # Print out final list    
    hemispheres_image_urls

