from flask import Flask, request, jsonify
from flask_cors import CORS
from helper import utils, colab_content
import traind_models, trained_models_1h


app = Flask(__name__)
CORS(app)  # Allow requests from frontend (important when frontend runs separately)

# Dummy model function (you will replace it later)
def predict_next_events(latitude, longitude, max_temp, gale, holiday, topic, date):
    # Later, you will load your trained ML model and predict here
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "Maximum Temperature (°C)": max_temp,
        "Gale": gale,
        "נושא": topic,
        "חג_עברי": holiday
    }

    predict_24h = colab_content.predict(payload, traind_models)
    predict_1h = colab_content.predict(payload, trained_models_1h)

    return {
        "1h_prediction":predict_1h,
        "24h_prediction":predict_24h
    }

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

# Predict route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    print(data)
    # Extract data from request
    settlement = data.get('settlement')
    latitude, longitude = utils.get_lat_lon(settlement_name=settlement)
    max_temp = 13   # hard-coded
    holiday = data.get('holiday')
    gale = 1
    topic = data.get('topic')
    date = data.get('date')

    # Call your prediction function
    prediction_result = predict_next_events(longitude, latitude, gale, max_temp, holiday, topic, date)

    # Return the prediction
    return jsonify(prediction_result)
if __name__ == "__main__":
    app.run(debug=True, port=5001)

