from flask import Flask, request, jsonify
from flask_cors import CORS
from helper import utils, colab_content
import os # Added for path joining if needed later, but not strictly required by fix

app = Flask(__name__)
CORS(app)

def predict_next_events(latitude, longitude, max_temp, gale, holiday, topic, date_str):
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "Maximum Temperature (°C)": max_temp, # Ensure this key matches model training
        "Gale": gale,
        "נושא": topic, # Ensure this key matches model training
        "חג_עברי": holiday, # Ensure this key matches model training
        "תאריך ושעה פתיחה": date_str # Ensure this key matches model training and datetime_col argument
    }
    print("--- Sending Payload ---")
    print(payload)

    # Assuming colab_content.predict correctly calls predict_next_event_probabilities
    # And handles potential errors internally or lets them propagate
    # Use payload.copy() if predict modifies the dictionary in place
    predict_24h = colab_content.predict(payload.copy(), "./trained_models_24h")
    predict_8h = colab_content.predict(payload.copy(), "./trained_models_8h")
    predict_1h = colab_content.predict(payload.copy(), "./trained_models_1h")

    return {
        "1h_prediction": predict_1h,
        "8h_prediction": predict_8h,
        "24h_prediction": predict_24h
    }

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    print("--- Received Request Data ---")
    print(data)

    settlement = data.get('settlement')
    holiday = data.get('holiday') # Assumes frontend sends 'holiday'
    topic = data.get('topic')
    date_input = data.get('date') # Assumes frontend sends 'date' as a string

    if not all([settlement, holiday, topic, date_input]):
        missing = [k for k,v in {'settlement': settlement, 'holiday': holiday, 'topic': topic, 'date': date_input}.items() if not v]
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        latitude, longitude = utils.get_lat_lon(settlement_name=settlement)
        if latitude is None or longitude is None:
             return jsonify({"error": f"Could not geocode settlement: {settlement}"}), 400
    except Exception as e:
        print(f"Geocoding error: {e}")
        return jsonify({"error": f"Error geocoding settlement: {settlement}"}), 500


    # Using hardcoded values as per original code - consider getting from request if needed
    max_temp = 13
    gale = 1

    try:
        prediction_result = predict_next_events(
            latitude,
            longitude,
            max_temp,
            gale,
            holiday, # Pass the holiday value
            topic,
            date_input # Pass the date string
        )
        return jsonify(prediction_result)
    except FileNotFoundError as e:
         print(f"Prediction error: Model files not found. {e}")
         return jsonify({"error": "Prediction models not found or path incorrect."}), 500
    except KeyError as e:
        print(f"Prediction error: Missing feature key in payload or during processing. {e}")
        return jsonify({"error": f"Missing expected data for prediction: {e}"}), 400
    except ValueError as e:
        print(f"Prediction error: Data format issue (e.g., datetime). {e}")
        return jsonify({"error": f"Invalid data format for prediction: {e}"}), 400
    except Exception as e:
        print(f"!!! Unexpected error during prediction call: {type(e).__name__}: {e}")
        # import traceback
        # traceback.print_exc() # Uncomment for detailed stack trace in logs
        return jsonify({"error": "An internal server error occurred during prediction."}), 500


if __name__ == "__main__":
    # Consider setting debug=False for production
    app.run(host='0.0.0.0', port=5001, debug=True)