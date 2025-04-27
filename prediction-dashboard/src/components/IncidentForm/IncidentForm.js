import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // בשביל ניתוב לדשבורד אחרי שליחה

const settlements = [
  "אביחיל",
  "אחיטוב",
  "אלישיב",
  "אומץ",
  "בארותיים",
  "בורגתה",
  "בית הלוי",
  "בית חרות",
  "בית ינאי",
  "בית יצחק",
  "ביתן אהרון",
  "גאולי תימן",
  "גבעת שפירא",
  "גן יאשיה",
  "הדר עם",
  "חבצלת השרון",
  "חוגלה",
  "חיבת ציון",
  "חניאל",
  "חרב לאת",
  'כפר הרא"ה',
  "כפר ויתקין",
  "כפר חיים",
  "כפר ידידיה",
  "כפר מונאש",
  "מכמורת",
  "עולש",
  "בחן",
  "גבעת חיים (איחוד)",
  "גבעת חיים (מאוחד)",
  "המעפיל",
  "העוגן",
  "מעברות",
  "משמר השרון",
  "עין החורש",
  "בת חפר",
  "בת חן",
  "חופית",
  "יד חנה",
  "צוקי ים",
  "שושנת העמקים",
];

function IncidentForm() {
  const [selectedSettlement, setSelectedSettlement] = useState("");
  const [date, setDate] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!settlements.includes(selectedSettlement)) {
      setError("בחר יישוב מהרשימה בלבד");
      return;
    }
    if (!date) {
      setError("בחר תאריך");
      return;
    }
    setError("");
    // ניווט לדשבורד
    navigate("/dashboard"); // נניח שהדאשבורד יושב בנתיב הזה
  };

  return (
    <div className="form-container">
      <h1 className="form-title">מוקד המועצה</h1>
      <form onSubmit={handleSubmit} className="form">
        <label className="form-label">
          יישוב המפגע:
          <input
            list="settlement-options"
            value={selectedSettlement}
            onChange={(e) => setSelectedSettlement(e.target.value)}
            className="form-input"
            required
          />
          <datalist id="settlement-options">
            {settlements.sort().map((settlement) => (
              <option key={settlement} value={settlement} />
            ))}
          </datalist>
        </label>

        <label className="form-label">
          תאריך:
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="form-input"
            required
          />
        </label>

        {error && <div className="form-error">{error}</div>}

        <button type="submit" className="submit-button">
          שלח
        </button>
      </form>
    </div>
  );
}

export default IncidentForm;
