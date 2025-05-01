import os
import sqlite3
import pymongo
from flask import Flask, jsonify, render_template, request
import pprint
from bson import ObjectId 
app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.acme_loans
applications = db.applications

print(client.list_database_names())
#applications.insert_one({"Name" : "silas", "Address" : 'address', "Status" : "received", "Notes" : []})

@app.route('/api/submitApp', methods=['POST'])
def submitApp():
    print("enter")
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    try:
        result = applications.insert_one({"Name" : name, "Address" : address, "Status" : "received", "Notes" : []})
        print(result.inserted_id)
        return jsonify({"status": "success", "application_id": str(result.inserted_id)})  
    except:
        print("error")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")