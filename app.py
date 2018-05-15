from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    #mars_data = mongo.db.data.find()
    return render_template("index.html")#, mars_data = mars_data)


@app.route("/scrape")
def scrape():
    data = mongo.db.data
    mars_data = scrape_mars.scrape()
    print("App.py: ", mars_data)
    print()
    #data.update({}, mars_data, upsert = True)
    return redirect("http://localhost:5000/", code = 302)


if __name__ == "__main__":
    app.run(debug=True)