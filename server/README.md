# Prediction API Server - Flask

This is the backend server for the Prediction Dashboard project.  
It is a simple Flask server that accepts form data and returns prediction results.

---

## 🚀 How to Run the Server

### 1. Navigate to the server folder:

```bash
cd server
```

### 2. Create a virtual environment:

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment:

- On Mac/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 4. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Run the Flask server:

```bash
python app.py
```

The server will run locally on:

```
http://localhost:5000
```

---

## 🛁 API Endpoints

### POST `/predict`

- **Description:**  
  Accepts settlement name, topic, and date from the frontend and returns a prediction.

- **Request Body Example:**

  ```json
  {
    "settlement": "Example Settlement",
    "topic": "Example Topic",
    "date": "2025-04-27"
  }
  ```

- **Response Example:**
  ```json
  {
    "currentCall": {
      "type": "Example Topic",
      "time": "14:30",
      "weather": "25°C, בהיר",
      "specialDay": "לא (יום חול רגיל)",
      "location": {
        "latitude": 32.3161,
        "longitude": 34.9066,
        "name": "Example Settlement"
      }
    },
    "predictions": {
      "oneHour": [...],
      "eightHours": [...],
      "twentyFourHours": [...]
    }
  }
  ```

---

## ⚙️ Project Files

```
server/
├── app.py             # Main Flask application
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 📒 Notes

- **CORS** is enabled (using `flask-cors`) to allow communication with the frontend.
- Predictions are currently static and should be replaced with a real model later.

---

## 👨‍💻 Developer Setup Checklist

- [x] Python 3 installed
- [x] Virtual environment activated
- [x] Required packages installed
- [x] Server running on port 5000
