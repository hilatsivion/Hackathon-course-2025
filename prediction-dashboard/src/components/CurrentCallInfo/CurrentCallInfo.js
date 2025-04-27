import React from "react";

function CurrentCallInfo({ type, time, weather, specialDay }) {
  return (
    <div className="card">
      <h2 className="card-title">נתוני הקריאה הנוכחית והסביבה</h2>
      <div className="dashboard-card-top">
        <div>
          <strong>סוג קריאה נוכחית:</strong> {type}
        </div>
        <div>
          <strong>שעת התרחשות:</strong> {time}
        </div>
      </div>
    </div>
  );
}

export default CurrentCallInfo;
