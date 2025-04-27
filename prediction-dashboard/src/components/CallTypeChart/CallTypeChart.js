import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart, BarElement, CategoryScale, LinearScale } from "chart.js";

Chart.register(BarElement, CategoryScale, LinearScale);

function CallTypeChart({ labels, data }) {
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "אחוז סיכוי",
        data: data,
        backgroundColor: [
          "rgba(59, 130, 246, 0.7)",
          "rgba(16, 185, 129, 0.7)",
          "rgba(239, 68, 68, 0.7)",
          "rgba(245, 158, 11, 0.7)",
        ],
        borderColor: [
          "rgba(59, 130, 246, 1)",
          "rgba(16, 185, 129, 1)",
          "rgba(239, 68, 68, 1)",
          "rgba(245, 158, 11, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    indexAxis: "y",
    scales: {
      x: { beginAtZero: true },
    },
    plugins: {
      legend: { display: false },
    },
    maintainAspectRatio: false,
  };

  return (
    <div className="card">
      <h2 className="card-title">איזה סוג קריאה?</h2>
      <div className="chart-container">
        <Bar data={chartData} options={options} />
      </div>
      <p>התפלגות סוגי הקריאות הצפויות.</p>
    </div>
  );
}

export default CallTypeChart;
