import React, { useEffect, useState } from "react";
import Header from "../../components/Header/Header";
import CurrentCallInfo from "../../components/CurrentCallInfo/CurrentCallInfo";
import LocationMap from "../../components/Map/LocationMap";
import DashboardCard from "../../components/DashboardCardPred/DashboardCardPred";
import PredictItem from "../../components/PredictItem/PredictItem";
import { fetchPredictionData } from "../../api/predictionApi";
import "./PrediPage.css";

function PredicationPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchPredictionData().then((response) => {
      setData(response);
    });
  }, []);

  if (!data) {
    return <div>טוען נתונים...</div>;
  }

  const { currentCall, predictions } = data;

  return (
    <>
      <Header />
      <div className="container">
        <h1 className="page-title">לוח מחוונים לחיזוי קריאות</h1>

        <CurrentCallInfo
          type={currentCall.type}
          time={currentCall.time}
          weather={currentCall.weather}
          specialDay={currentCall.specialDay}
        />

        <div className="cards-container-pred">
          <DashboardCard title="קריאות צפויות לשעה הקרובה">
            {predictions.oneHour.map((item, index) => (
              <PredictItem
                key={index}
                label={item.label}
                percentage={item.percentage}
              />
            ))}
          </DashboardCard>

          <DashboardCard title="קריאות צפויות ל-8 השעות הקרובות">
            {predictions.eightHours.map((item, index) => (
              <PredictItem
                key={index}
                label={item.label}
                percentage={item.percentage}
              />
            ))}
          </DashboardCard>

          <DashboardCard title="קריאות צפויות ל-24 השעות הקרובות">
            {predictions.twentyFourHours.map((item, index) => (
              <PredictItem
                key={index}
                label={item.label}
                percentage={item.percentage}
              />
            ))}
          </DashboardCard>
        </div>

        <LocationMap
          latitude={currentCall.location.latitude}
          longitude={currentCall.location.longitude}
          name={currentCall.location.name}
        />
      </div>
    </>
  );
}

export default PredicationPage;
