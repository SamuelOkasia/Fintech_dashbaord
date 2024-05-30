from flask import Blueprint, jsonify, request, current_app
import subprocess
from app.models import FinancialData
from app import db
from datetime import datetime
import json
import os

page_blueprint = Blueprint('Page', __name__)

@page_blueprint.route('/monthly_profits_losses_page', methods=['GET'])
def monthly_profits_losses_page():
    # Adjust the base directory to the project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    c_program_path = os.path.join(base_dir,'app', 'c_programs', 'monthly_profits_losses.exe')


    # Print out the path to debug
    print(f"Constructed C program path: {c_program_path}")

    # Ensure the path is correct and the file exists
    if not os.path.isfile(c_program_path):
        print(f"File not found: {c_program_path}")
        return jsonify({"error": "C program executable not found", "path": c_program_path}), 404

    # Call the C program and capture its output
    try:
        result = subprocess.run([c_program_path], capture_output=True, text=True)
        result.check_returncode()  # This will raise an error if the C program didn't exit cleanly
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error running C program: {str(e)}"}), 500

    # Parse the JSON output from the C program
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Error parsing JSON output: {str(e)}"}), 500

    # Prepare data for the frontend
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    profits = [0] * 12
    losses = [0] * 12

    for entry in data:
        month_index = entry['month'] - 1
        profits[month_index] = entry['profit']
        losses[month_index] = entry['loss']

    response = {
        'labels': labels,
        'profits': profits,
        'losses': losses
    }

    return jsonify(response)

@page_blueprint.route('/monthly_revenue_data', methods=['GET'])
def monthly_revenue_data():
    # Adjust the base directory to include the app directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    c_program_path = os.path.join(base_dir,'app', 'c_programs', 'monthly_profits_losses.exe')

    # Print out the path to debug
    print(f"Constructed C program path: {c_program_path}")

    # Ensure the path is correct and the file exists
    if not os.path.isfile(c_program_path):
        print(f"File not found: {c_program_path}")
        return jsonify({"error": "C program executable not found", "path": c_program_path}), 404

    # Call the C program and capture its output
    try:
        result = subprocess.run([c_program_path], capture_output=True, text=True)
        result.check_returncode()  # This will raise an error if the C program didn't exit cleanly
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error running C program: {str(e)}"}), 500

    # Parse the JSON output from the C program
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Error parsing JSON output: {str(e)}"}), 500

    return jsonify(data)