import React from "react";
import "./DashboardCard.css";

function DashboardCard({ title, children }) {
  return (
    <div className="dashboard-card">
      <div className="dashboard-card-header">{title}</div>
      <div className="dashboard-card-content">{children}</div>
    </div>
  );
}

export default DashboardCard;
