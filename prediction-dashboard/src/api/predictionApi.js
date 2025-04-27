export const fetchPredictionData = () => {
  return Promise.resolve({
    currentCall: {
      type: "תקלה טכנית",
      time: "14:30",
      weather: "25°C, בהיר",
      specialDay: "לא (יום חול רגיל)",
      location: {
        latitude: 32.3161,
        longitude: 34.9066,
        name: "חבצלת השרון",
      },
    },
    predictions: {
      oneHour: [
        { label: "חתולים משוטטים", percentage: 90 },
        { label: "דבורים מעופפים", percentage: 40 },
        { label: "אי זריקת פחים ירוקים", percentage: 10 },
      ],
      eightHours: [
        { label: "חתולים משוטטים", percentage: 90 },
        { label: "דבורים מעופפים", percentage: 20 },
        { label: "אי זריקת פחים ירוקים", percentage: 10 },
      ],
      twentyFourHours: [
        { label: "חתולים משוטטים", percentage: 60 },
        { label: "אי זריקת פחים ירוקים", percentage: 10 },
      ],
    },
  });
};

// דוגמה לקריאת API לשרת פלאסק
/*
const sendFormData = async (settlement, topic, date) => {
  try {
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        settlement: settlement,
        topic: topic,
        date: date,
      }),
    });

    if (!response.ok) {
      throw new Error("בעיה בשליחת הנתונים לשרת");
    }

    const data = await response.json();
    console.log("קיבלנו תשובה מהשרת:", data);

    // כאן אפשר לעשות:
    // setData(data);
    // או navigate("/dashboard", { state: data });

    return data;
  } catch (error) {
    console.error("שגיאה בקריאה לשרת:", error);
    throw error;
  }
};
*/
