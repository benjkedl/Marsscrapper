# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.mars_scrape.find_one()
    
    # return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrapper():

    # Run scraped functions
    mars_scrape = scrape.scrape()

    # Insert forecast into database
    mongo.db.mars_scrape.update({}, mars_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)