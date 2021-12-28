# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set the executable path and start Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and svve it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ## Mars Facts

# Create dataframe containing mars facts from the website
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Define the columns for the dataframe
df.columns=['Description', 'Mars', 'Earth']
# Redefine index as description column
df.set_index('Description', inplace=True)
df

# Transform dataframe to HTML code
df.to_html()

# ## D1: Scrape High Resolution Image of Mars' Hemispheres with Titles

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

browser.visit(url)

# 3. Write code to retrieve the image urls and titles for each hemisphere.\
hemi_links = browser.find_by_css('a.product-item img')
# Create loop to go through links
for i in range (len(hemi_links)):
    # Create dictionary for image url and title 
    hemi_image_dicts = {}
    # Capture image and go to next page
    browser.find_by_css('a.product-item img')[i].click()
    # Go to page with sample image and extract
    sample_elem = browser.find_by_text('Sample').first
    hemi_image_dicts['img_url'] = sample_elem['href']
    # Extract title
    hemi_image_dicts['title'] = browser.find_by_css('h2.title').text
    # Extract description from hemisphere
    hemi_image_dicts['descrip'] = browser.find_by_css('p').text
    # Add dictionary items to list
    hemisphere_image_urls.append(hemi_image_dicts)
    # Return back to main page
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

browser.quit()
