from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    records = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=records)


@app.route("/scrape")
def scraper():
    mongo.db.mars_data.drop()
    mars_data = mongo.db.mars_data
    current_mars_data = scrape_mars.scrape()
    mars_data.insert(current_mars_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)