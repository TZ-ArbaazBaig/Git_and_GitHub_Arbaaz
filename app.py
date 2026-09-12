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

todos_collection = db["todos"]

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



@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        if request.is_json:
            data = request.get_json()

            item_name = data.get("itemName")
            item_description = data.get("itemDescription")

        else:
            item_name = request.form.get("itemName")
            item_description = request.form.get("itemDescription")

        if not item_name or not item_description:
            return jsonify({
                "error": "itemName and itemDescription are required"
            }), 400

        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        result = todos_collection.insert_one(todo_item)

        return jsonify({
            "message": "Todo item submitted successfully",
            "id": str(result.inserted_id)
        }), 201

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
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )