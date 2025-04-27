from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # מאפשר קריאות מה-Frontend

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    settlement = data.get('settlement')
    topic = data.get('topic')
    date = data.get('date')

    # כרגע נחזיר תשובה דמיונית (נחליף במודל אמיתי אחר כך)
    prediction = {
        "currentCall": {
            "type": topic,
            "time": "14:30",
            "weather": "25°C, בהיר",
            "specialDay": "לא (יום חול רגיל)",
            "location": {
                "latitude": 32.3161,
                "longitude": 34.9066,
                "name": settlement,
            },
        },
        "predictions": {
            "oneHour": [
                {"label": "חתולים משוטטים", "percentage": 90},
                {"label": "דבורים מעופפים", "percentage": 40},
                {"label": "אי זריקת פחים ירוקים", "percentage": 10},
            ],
            "eightHours": [
                {"label": "חתולים משוטטים", "percentage": 90},
                {"label": "דבורים מעופפים", "percentage": 20},
                {"label": "אי זריקת פחים ירוקים", "percentage": 10},
            ],
            "twentyFourHours": [
                {"label": "חתולים משוטטים", "percentage": 60},
                {"label": "אי זריקת פחים ירוקים", "percentage": 10},
            ],
        },
    }

    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
