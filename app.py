from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise ValueError("MONGODB_URI is not set in the .env file")

client = MongoClient(MONGO_URI)

db = client["flask_mongodb_db"]
collection = db["users"]


@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            if not name or not email or not message:
                return render_template(
                    "index.html",
                    error="All fields are required."
                )

            collection.insert_one({
                "name": name,
                "email": email,
                "message": message
            })

            return redirect(url_for("success"))

        except Exception as error:

            return render_template(
                "index.html",
                error=str(error)
            )

    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)