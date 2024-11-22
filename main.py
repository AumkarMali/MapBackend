from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://aum:Sept2020@cluster0.jvtzn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

app = Flask(__name__)
CORS(app)

# Access the database and collection
db = client["user_list"]
collection = db["tasks"]

def add_user(username, password):
    # Create the document to insert
    user_data = {
        "username": username,
        "password": password
    }

    # Insert the document into the collection
    try:
        result = collection.insert_one(user_data)
        print(f"User added with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Failed to insert user: {e}")

@app.route('/api/data', methods=['POST'])
def add_user_route():
    # Retrieve JSON data from the request body
    data = request.get_json()

    # Extract username and password
    un = data.get('username')
    ps = data.get('password')

    # Add the user to the database
    add_user(username=un, password=ps)

    return jsonify({"message": "User added successfully"}), 201

@app.route('/api/check', methods=['POST'])
def check_user():
    # Retrieve JSON data from the request body
    data = request.get_json()

    # Extract username and password
    un = data.get('username')
    ps = data.get('password')

    # Check if the username exists in the database
    user = collection.find_one({"username": un})

    if user:
        # Check if the password matches
        if user["password"] == ps:
            return jsonify({"exists": True}), 200
        else:
            return jsonify({"exists": False, "message": "Incorrect password"}), 401
    else:
        return jsonify({"exists": False, "message": "Username not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
