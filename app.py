from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

DB_FILE = "reports.json"  # File where reports will be saved

# Load existing reports from the file
def load_reports():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty list

# Save reports to the file
def save_reports(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Endpoint to submit a report
@app.route('/report', methods=['POST'])
def report_issue():
    data = request.json  # Get the JSON data from the request

    # Format the report data
    report_data = {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "description": data.get("description"),
        "type": data.get("type", "Other"),  # Default type is 'Other' if not provided
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat())  # Use current timestamp if not provided
    }

    # Load existing reports
    reports = load_reports()

    # Add the new report to the list
    reports.append(report_data)

    # Save the updated list of reports
    save_reports(reports)

    # Return a success response
    return jsonify({"message": "Report submitted successfully!"}), 200

# Endpoint to get all reports
@app.route('/reports', methods=['GET'])
def get_reports():
    reports = load_reports()  # Load the reports
    return jsonify(reports)  # Return reports as a JSON response

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
