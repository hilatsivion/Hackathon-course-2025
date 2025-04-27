import React from "react";
import Header from "../../components/Header/Header";
import CurrentCallInfo from "../../components/CurrentCallInfo/CurrentCallInfo";
import LocationMap from "../../components/Map/LocationMap";
import DashboardCard from "../../components/DashboardCardPred/DashboardCardPred";
import PredictItem from "../../components/PredictItem/PredictItem";
import "./PrediPage.css";

function PredicationPage() {
  return (
    <>
      <Header />

      <div className="container">
        <h1 className="page-title">לוח מחוונים לחיזוי קריאות</h1>
        <CurrentCallInfo
          type="תקלה טכנית"
          time="14:30"
          weather="25°C, בהיר"
          specialDay="לא (יום חול רגיל)"
        />
        <div className="cards-container-pred">
          <DashboardCard title="קריאות צפויות לשעה הקרובה">
            <PredictItem label="חתולים משוטטים" percentage={90} />
            <PredictItem label="דבורים מעופפים" percentage={40} />
            <PredictItem label="אי זריקת פחים ירוקים" percentage={10} />
          </DashboardCard>
          <DashboardCard title="קריאות צפויות ל-8 השעות הקרובות">
            <PredictItem label="חתולים משוטטים" percentage={90} />
            <PredictItem label="דבורים מעופפים" percentage={20} />
            <PredictItem label="אי זריקת פחים ירוקים" percentage={10} />{" "}
          </DashboardCard>
          <DashboardCard title="קריאות צפויות ל-24 השעות הקרובות">
            <PredictItem label="חתולים משוטטים" percentage={60} />
            <PredictItem label="אי זריקת פחים ירוקים" percentage={10} />{" "}
          </DashboardCard>
        </div>
        <div>
          <LocationMap
            latitude={32.3161}
            longitude={34.9066}
            name="חבצלת השרון"
          />
        </div>
        <div className="cards-grid"></div>
      </div>
    </>
  );
}

export default PredicationPage;
