from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = os.environ.get('authentication')
#mongo = PyMongo(app)

##Use flaask_pymongo to set up connection locally
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"
mongo = PyMongo(app)


@app.route("/")
def home():
    ## write a statement that finds all the items in the db and sets it to a variable
    mars_info = mongo.db.mars_info.find()
    print(mars_info[0])
    ## render an index.html template and pass it the data you retrieved from the database 
    return render_template("index.html", mars_info=mars_info[0])


@app.route("/scrape")
def scraper():
    ## reference the collection
    mars_info = mongo.db.mars_info
    ## run the scrape function
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    return "Scraping Done."


if __name__ == "__main__":
    app.run()


