import React from "react";

function TimePrediction({ hours }) {
  return (
    <div className="card">
      <h2 className="card-title">מתי הקריאה הבאה?</h2>
      <div className="result-text">~ {hours} שעות</div>
      <p>זמן מוערך מהקריאה הנוכחית.</p>
    </div>
  );
}

export default TimePrediction;
