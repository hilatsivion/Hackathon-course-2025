import React from "react";

function CurrentCallInfo({ type, time, weather, specialDay }) {
  return (
    <div className="card">
      <h2 className="card-title">נתוני הקריאה הנוכחית והסביבה</h2>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-around",
          marginTop: "20px",
        }}
      >
        <div>
          <strong>סוג קריאה נוכחית:</strong> {type}
        </div>
        <div>
          <strong>שעת התרחשות:</strong> {time}
        </div>
        <div>
          <strong>מזג אוויר:</strong> {weather}
        </div>
        <div>
          <strong>יום מיוחד:</strong> {specialDay}
        </div>
      </div>
    </div>
  );
}

export default CurrentCallInfo;
