from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    news_data = mongo.db.mars_data.find_one({'title' : 'Latest Mars News'})
    featured_data = mongo.db.mars_data.find_one({'title' : 'Featured Image'})
    weather_data = mongo.db.mars_data.find_one({'title' : 'Weather on Mars'})
    facts_data = mongo.db.mars_data.find_one({'title' : 'Facts About Mars'})
    hemi1_data = mongo.db.mars_data.find_one({'title' : 'Cerberus Hemisphere'})
    hemi2_data = mongo.db.mars_data.find_one({'title' : 'Schiaparelli Hemisphere'})
    hemi3_data = mongo.db.mars_data.find_one({'title' : 'Syrtis Major Hemisphere'})
    hemi4_data = mongo.db.mars_data.find_one({'title' : 'Valles Marineris Hemisphere'})
    return render_template("index.html", news_data = news_data, featured_data = featured_data, weather_data = weather_data,
                          facts_data = facts_data, hemi1_data = hemi1_data, hemi2_data = hemi2_data, hemi3_data = hemi3_data,
                          hemi4_data = hemi4_data)


@app.route("/scrape")
def scrape():
    mongo.db.mars_data.drop()
    mars_data = mongo.db.mars_data
    data = scrape_mars.scrape()
    mars_data.insert_many(data)
    return redirect("http://localhost:5000/", code = 302)


if __name__ == "__main__":
    app.run(debug=True)