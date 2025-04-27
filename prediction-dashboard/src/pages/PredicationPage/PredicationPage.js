import React from "react";
import { useLocation } from "react-router-dom";
import Header from "../../components/Header/Header";
import CurrentCallInfo from "../../components/CurrentCallInfo/CurrentCallInfo";
import LocationMap from "../../components/Map/LocationMap";
import DashboardCard from "../../components/DashboardCardPred/DashboardCardPred";
import PredictItem from "../../components/PredictItem/PredictItem";
import settlementCoordinates from "./settlementCoordinates";

import "./PrediPage.css";

function PredicationPage() {
  const location = useLocation();
  const { predictionData, userSelection } = location.state || {};

  if (
    !predictionData ||
    !predictionData["1h_prediction"] ||
    !predictionData["24h_prediction"]
  ) {
    return <div>אין נתונים להצגה</div>;
  }

  const { currentCall } = predictionData;

  const predictions = {
    oneHour: Object.entries(predictionData["1h_prediction"] || {}).map(
      ([label, percentage]) => ({
        label,
        percentage: percentage * 100,
      })
    ),
    eightHours: Object.entries(predictionData["8h_prediction"] || {}).map(
      ([label, percentage]) => ({
        label,
        percentage: percentage * 100,
      })
    ),
    twentyFourHours: Object.entries(predictionData["24h_prediction"] || {}).map(
      ([label, percentage]) => ({
        label,
        percentage: percentage * 100,
      })
    ),
  };

  return (
    <>
      <Header />
      <div className="container">
        <h1 className="page-title">לוח מחוונים לחיזוי קריאות</h1>

        {userSelection && (
          <CurrentCallInfo
            type={userSelection.selectedTopic}
            time={new Date(userSelection.date).toLocaleString("he-IL")}
          />
        )}

        <div className="cards-container-pred">
          <DashboardCard title="קריאות צפויות לשעה הקרובה">
            {predictions.oneHour
              ?.sort((a, b) => b.percentage - a.percentage)
              .slice(0, 3)
              .map((item, index) => (
                <PredictItem
                  key={index}
                  label={item.label}
                  percentage={item.percentage.toFixed(0)}
                />
              ))}
          </DashboardCard>

          <DashboardCard title="קריאות צפויות ל-8 השעות הקרובות">
            {predictions.eightHours
              ?.sort((a, b) => b.percentage - a.percentage)
              .slice(0, 3)
              .map((item, index) => (
                <PredictItem
                  key={index}
                  label={item.label}
                  percentage={item.percentage.toFixed(0)}
                />
              ))}
          </DashboardCard>

          <DashboardCard title="קריאות צפויות ל-24 השעות הקרובות">
            {predictions.twentyFourHours
              ?.sort((a, b) => b.percentage - a.percentage)
              .slice(0, 3)
              .map((item, index) => (
                <PredictItem
                  key={index}
                  label={item.label}
                  percentage={item.percentage.toFixed(0)}
                />
              ))}
          </DashboardCard>
        </div>

        {userSelection &&
          settlementCoordinates[userSelection.selectedSettlement] && (
            <LocationMap
              latitude={
                settlementCoordinates[userSelection.selectedSettlement].latitude
              }
              longitude={
                settlementCoordinates[userSelection.selectedSettlement]
                  .longitude
              }
              name={userSelection.selectedSettlement}
            />
          )}
      </div>
    </>
  );
}

export default PredicationPage;
