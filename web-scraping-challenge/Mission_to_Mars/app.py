from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)





@app.route("/")
def index():
    display_mars = mongo.db.display_mars.find_one()
    return render_template("scrape_render.html", display_mars=display_mars)


#@app.route("/scrape")
def scraper():
    display_mars = mongo.db.display_mars
    display_mars_data = scrape_mars.scrape()
    display_mars.update({}, display_mars_data, upsert=True)
    return redirect("/", code=302)   








if __name__ == "__main__":
    app.run(debug=True)