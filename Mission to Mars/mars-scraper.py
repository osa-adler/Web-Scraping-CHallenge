from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def scrape():
    # Splinter Setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Main Dictionary
    mars_dict = {}

    # URL to visit
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Latest News Title and Paragraph Text
    news_title = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text
    news_paragraph = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text

    # Append to dictionary
    mars_dict['News_Title'] = news_title
    mars_dict['News_Paragraph'] = news_paragraph

    # URL for Images
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Click full image button
    browser.find_by_text(' FULL IMAGE').click()

    # Xpath for Img
    featured_image_url = browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')['src']

    # Append to dictionary
    mars_dict['Featured_Img_URL'] = featured_image_url

    # URL for tables
    url = 'https://galaxyfacts-mars.com/'

    # Table for Earth and Mars Comparison
    tables = pd.read_html(url)
    two_df = tables[0]
    two_df = two_df.rename(columns={0:'Values',
                                        1: 'Mars',
                                            2: 'Earth'})
    two_df = two_df.set_index('Values')

    # HTML for comparison table
    mars_html = two_df.to_html(classes="table table-striped")
    mars_html = mars_html.replace('\n', '')

    # Append to dictionary
    mars_dict['mars_table'] = mars_html

    # URL for Mars Hemisphere Imgs and Titles
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Scrape for Title and full img href 
    full_href = []

    for i in range(1,4):
        url_titles = {}

        # Copied the xpath of the clickable <h3> to click for full img and loop through for all four
        xpath = '//*[@id="product-section"]/div[2]/div[' + str(i) + ']/div/a/h3'
        browser.find_by_xpath(xpath).click()

        # Saved copied xpath for full_img and title
        full_img = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')['href']
        img_title = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
    
        # Create dictionaries
        url_titles['img_url'] = full_img
        url_titles['title'] = img_title

        # Append dictionaries to full_href
        full_href.append(url_titles)

        # Return to previous page for next loop
        browser.back()

    # Append to dictionary    
    mars_dict['Full_url_and_title'] = full_href

    browser.quit()

    return mars_dict
