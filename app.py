from flask import Flask, render_template, request, jsonify
import prediction
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# API listening to POST requests and predicting sentiments
@app.route('/predict', methods=['POST'])
def predict():
    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status': 'error', 'message': 'Empty Review'}
    else:
        # calling the predict method from prediction.py module
        sentiment, path = prediction.predict(review)
        response = {'status': 'success',
                    'message': 'Got it',
                    'sentiment': sentiment,
                    'path': path}
    return jsonify(response)

# Creating an API to save the review when the user clicks on the Save button
@app.route('/save', methods=['POST'])
def save():
    try:
        # Extracting data from JSON request
        date = request.json.get('date')
        product = request.json.get('product')
        review = request.json.get('review')
        sentiment = request.json.get('sentiment')

        # Creating a CSV-like entry
        data_entry = f"{date},{product},{review},{sentiment}"

        # Logging data to a file
        with open('log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_entry.split(','))

        # Return a success message
        return jsonify({'status': 'success', 'message': 'Data Logged'})

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
