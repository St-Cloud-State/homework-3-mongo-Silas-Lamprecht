import os
import pymongo
from flask import Flask, jsonify, render_template, request
from bson import ObjectId

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.acme_loans
applications = db.applications


@app.route('/api/submitApp', methods=['POST'])
def submitApp():
    print("enter")
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    try:
        result = applications.insert_one({"Name" : name, "Address" : address, "Status" : "received", "Notes" : []})
        print(result.inserted_id)
        return jsonify({"status": "received", "application_id": str(result.inserted_id)})  
    except:
        print("error")





@app.route('/api/checkStatus/<application_id>', methods=['GET'])
def check_status(application_id):
    try:
        application = applications.find_one({"_id": ObjectId(application_id)})
        if application:
            return jsonify({
                "status": "success",
                "_id": str(application["_id"]),
                "application_status": application.get("Status", ""),
                "notes": application.get("Notes", [])
            })
        else:
            return jsonify({"status": "error", "message": "Application not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    application_id = data.get('_id')  # expected to be a string
    new_status = data.get('status')
    note = data.get('note')  # optional

    if not application_id or not new_status:
        return jsonify({"error": "Missing required fields"}), 400

    update_fields = {"Status": new_status}
    if note:
        update_fields["$push"] = {"Notes": note}

    try:
        result = applications.update_one(
            {"_id": ObjectId(application_id)},
            {
                "$set": {"Status": new_status},
                **({"$push": {"Notes": note}} if note else {})
            }
        )
        if result.matched_count == 0:
            return jsonify({"error": "Application not found"}), 404
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/api/add_subphase', methods=['POST'])
def add_subphase():
    data = request.get_json()
    application_id = data.get('_id')
    subphase_name = data.get('subphase_name')
    if not application_id or not subphase_name:
        return jsonify({"error": "Missing application_id or subphase_name"}), 400

    try:
        # Adding the subphase if it does not exist
        result = applications.update_one(
            {"_id": ObjectId(application_id)},
            {"$setOnInsert": {"subphases": []}},
            upsert=True
        )

        applications.update_one(
            {"_id": ObjectId(application_id)},
            {"$push": {"subphases": {"name": subphase_name, "tasks": []}}}
        )
        return jsonify({"status": "subphase added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    application_id = data.get('_id')
    subphase_name = data.get('subphase_name')
    task_name = data.get('task_name')
    print(application_id,subphase_name,task_name)
    if not application_id or not subphase_name or not task_name:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Add task to the correct subphase
        result = applications.update_one(
            {"_id": ObjectId(application_id), "subphases.name": subphase_name},
            {"$push": {"subphases.$.tasks": {"name": task_name, "status": "in-progress", "messages": []}}}
        )
        return jsonify({"status": "task added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/update_task_status', methods=['POST'])
def update_task_status():
    data = request.get_json()
    application_id = data.get('_id')
    subphase_name = data.get('subphase_name')
    task_name = data.get('task_name')
    status = data.get('status')
    message = data.get('message', "")

    if not application_id or not subphase_name or not task_name or not status:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        update_fields = {
            "subphases.$[subphase].tasks.$[task].status": status,
            "subphases.$[subphase].tasks.$[task].messages": message
        }
        result = applications.update_one(
            {"_id": ObjectId(application_id)},
            {
                "$set": update_fields
            },
            array_filters=[{"subphase.name": subphase_name}, {"task.name": task_name}]
        )
        return jsonify({"status": "task updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")