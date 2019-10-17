from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import pymongo

display_mars = {}

def init_browser():
    
    executable_path = {"executable_path": "Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    browser = init_browser()
    display_mars = {}

    url_titleandparagraph = 'https://mars.nasa.gov/news/'
    browser.visit(url_titleandparagraph)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #TITLE AND PARAGRAPH
    display_mars['news_titles'] = soup.title.text.strip()
    display_mars['news_paragraphs'] = soup.find('div', class_="article_teaser_body").text
    #news_paragraphs = news_paragraphs.text.strip()

    url_featuredimages = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_featuredimages)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #FEATURED IMAGE
    display_mars['featuredimage'] = soup.find_all('img')[69]

    url_marsweather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_marsweather)   
    html = browser.html
    soup = bs(html, 'html.parser')
    #MARS WEATHER
    display_mars['weather_image'] = soup.find_all('img')[4]

    url_marsfacts = 'https://space-facts.com/mars/'
    #browser.visit(url_marsfacts)   
    #html = browser.html
    tables = pd.read_html(url_marsfacts)
    df = tables[0]
    df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    df.set_index('Mars - Earth Comparison', inplace=True)

    df_mars = df.to_html()
    display_mars['df_mars'] = df_mars.replace('\n', '')

    url_hemispherecerberus = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url_hemispherecerberus)   
    html = browser.html
    soup = bs(html, 'html.parser')
    display_mars['cerberusimage'] = soup.find_all('li')[0]
    display_mars['cerberustitle'] = soup.title.text.strip()

    url_schiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url_schiaparelli)   
    html = browser.html
    soup = bs(html, 'html.parser')
    display_mars['schiaparelli_image'] = soup.find_all('li')[0]
    display_mars['schiaparellititle'] = soup.title.text.strip()

    url_syrtis_major = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url_syrtis_major)   
    html = browser.html
    soup = bs(html, 'html.parser')
    display_mars['syrtis_major_image'] = soup.find_all('li')[0]
    display_mars['syrtis_majortitle'] = soup.title.text.strip()

    url_valles_marineris = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url_valles_marineris)   
    html = browser.html
    soup = bs(html, 'html.parser')
    display_mars['valles_marineris_image'] = soup.find_all('li')[0]
    display_mars['valles_marineristitle'] = soup.title.text.strip()

    #hemisphere_image_urls = [
    #    {"title": valles_marineristitle, "img_url": valles_marineris_image},
    #    {"title": cerberustitle, "img_url": cerberusimage},
    #    {"title": schiaparellititle, "img_url": schiaparelli_image},
    #    {"title": syrtis_majortitle, "img_url": syrtis_major_image}]




    return display_mars

















#* Use Pymongo for CRUD applications for your database. For this homework, you can simply overwrite the existing document each time the `/scrape` url is visited and new data is obtained.

#* Use Bootstrap to structure your HTML template.






if __name__ == "__main__":
    app.run(debug=True)