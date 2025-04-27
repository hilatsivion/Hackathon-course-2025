import React from "react";
import "./PredictItem.css";

function PredictItem({ label, percentage }) {
  let backgroundColor = "";

  if (percentage >= 40) {
    backgroundColor = "#F9B6B6"; // אדום בהיר
  } else if (percentage >= 10) {
    backgroundColor = "#FFCCB1"; // כתום בהיר
  } else {
    backgroundColor = "#FFFAC5"; // צהוב בהיר
  }

  return (
    <div className="predict-item" style={{ backgroundColor }}>
      <div className="predict-item-label">{label}</div>
      <div className="predict-item-circle">{percentage}%</div>
    </div>
  );
}

export default PredictItem;
