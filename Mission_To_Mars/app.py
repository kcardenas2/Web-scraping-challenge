#Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Flask
app = Flask(__name__)
# Connection with mongo
conn= "mongodb://localhost:27017"
client =pymongo.MongoClient(conn)
db = client.mars_db


@app.route("/")
def index():
    mars_collection = db.dict.find_one()
    return render_template("index.html", mars=mars_collection)



@app.route("/scrape")
def scrape():
    dict= scrape_mars.scrape()
    db.dict.update({},dict, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)