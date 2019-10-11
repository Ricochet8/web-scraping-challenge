from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)




def init_browser():
    
    executable_path = {"executable_path": "Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    display_dict = {}

    url_titleandparagraph = 'https://mars.nasa.gov/news/'
    browser.visit(url_titleandparagraph)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.title.text.strip()
    news_paragraphs = soup.find('div', class_="article_teaser_body")
    news_paragraphs = news_paragraphs.text.strip()

    url_featuredimages = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_featuredimages)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    featuredimage = soup.find_all('img')[69]

    url_marsweather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_marsweather)   
    html = browser.html
    soup = bs(html, 'html.parser')
    weather_image = soup.find_all('img')[4]

    url_marsfacts = 'https://space-facts.com/mars/'
    browser.visit(url_marsfacts)   
    html = browser.html
    tables = pd.read_html(url_marsfacts)
    df = tables[0]
    df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    df.set_index('Mars - Earth Comparison', inplace=True)

    url_hemispherecerberus = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url_hemispherecerberus)   
    html = browser.html
    soup = bs(html, 'html.parser')
    cerberusimage = soup.find_all('li')[0]
    cerberustitle = soup.title.text.strip()

    url_schiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url_schiaparelli)   
    html = browser.html
    soup = bs(html, 'html.parser')
    schiaparelli_image = soup.find_all('li')[0]
    schiaparellititle = soup.title.text.strip()

    url_syrtis_major = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url_syrtis_major)   
    html = browser.html
    soup = bs(html, 'html.parser')
    syrtis_major_image = soup.find_all('li')[0]
    syrtis_majortitle = soup.title.text.strip()

    url_valles_marineris = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url_valles_marineris)   
    html = browser.html
    soup = bs(html, 'html.parser')
    valles_marineris_image = soup.find_all('li')[0]
    valles_marineristitle = soup.title.text.strip()

    hemisphere_image_urls = [
        {"title": valles_marineristitle, "img_url": valles_marineris_image},
        {"title": cerberustitle, "img_url": cerberusimage},
        {"title": schiaparellititle, "img_url": schiaparelli_image},
        {"title": syrtis_majortitle, "img_url": syrtis_major_image},


        {"Main title": news_title, "paragraph": news_paragraphs},
        {"Featured Image": featuredimage},
        {"weather image": weather_image},
        {"Table": df}
]
    return display_dict.append(hemisphere_image_urls)

# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.mars_db
# Drops collection if available to remove duplicates
db.mars.drop()
# Creates a collection in the database and inserts two documents
db.mars.insert_many(
    [
        {
            'player': 'Jessica',
            'position': 'Point Guard'
        },
        {
            'player': 'Mark',
            'position': 'Center'
        }
    ]
)

# Set route CHANGE VARIABLES
@app.route('/')
def index():
    # Store the entire team collection in a list
    teams = list(db.team.find())
    print(teams)

    # Return the template with the teams list passed in
    return render_template('index.html', teams=teams)






















if __name__ == "__main__":
    app.run(debug=True)