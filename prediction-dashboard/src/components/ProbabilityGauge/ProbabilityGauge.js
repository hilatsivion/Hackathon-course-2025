import React from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart, ArcElement, Tooltip, Legend } from "chart.js";

Chart.register(ArcElement, Tooltip, Legend);

function ProbabilityGauge({ probability }) {
  const data = {
    datasets: [
      {
        data: [probability * 100, 100 - probability * 100],
        backgroundColor: ["#3b82f6", "#e5e7eb"],
        borderWidth: 0,
        circumference: 180,
        rotation: 270,
      },
    ],
  };

  const options = {
    cutout: "70%",
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  };

  return (
    <div className="card">
      <h2 className="card-title">האם צפויה קריאה נוספת?</h2>
      <div className="chart-container">
        <Doughnut data={data} options={options} />
      </div>
      <div className="result-text">{Math.round(probability * 100)}%</div>
      <p>הסתברות לקריאה נוספת ב-24 השעות הקרובות.</p>
    </div>
  );
}

export default ProbabilityGauge;
