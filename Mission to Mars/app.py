# MongoDB and Flask Application


# Import dependencies for the app
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():

    # Run the scrape function from the scrape_mars.py file and save the results into a variable
    mars_scrape = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update_one({}, {"$set": mars_scrape}, upsert=True)

    # Redirect back to the home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
