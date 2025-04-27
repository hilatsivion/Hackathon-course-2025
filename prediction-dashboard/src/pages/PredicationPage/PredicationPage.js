import React from "react";
import { useLocation } from "react-router-dom";
import Header from "../../components/Header/Header";
import CurrentCallInfo from "../../components/CurrentCallInfo/CurrentCallInfo";
import LocationMap from "../../components/Map/LocationMap";
import DashboardCard from "../../components/DashboardCardPred/DashboardCardPred";
import PredictItem from "../../components/PredictItem/PredictItem";
import "./PrediPage.css";

function PredicationPage() {
  const location = useLocation();
  const { predictionData } = location.state || {};

  if (!predictionData.currentCall || !predictionData.predictions) {
    return <div>אין נתונים להצגה</div>;
  }

  if (
    !predictionData ||
    !predictionData.currentCall ||
    !predictionData.predictions
  ) {
    return <div>לא התקבלו נתונים להצגה</div>;
  }

  const { currentCall, predictions } = predictionData;

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

          {/* <DashboardCard title="קריאות צפויות ל-8 השעות הקרובות">
            {predictions.eightHours.map((item, index) => (
              <PredictItem
                key={index}
                label={item.label}
                percentage={item.percentage}
              />
            ))}
          </DashboardCard> */}

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
