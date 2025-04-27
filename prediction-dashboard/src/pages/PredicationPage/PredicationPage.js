import React from "react";
import Header from "../../components/Header/Header";
import ProbabilityGauge from "../../components/ProbabilityGauge/ProbabilityGauge";
import CallTypeChart from "../../components/CallTypeChart/CallTypeChart";
import TimePrediction from "../../components/TimePrediction/TimePrediction";
import CurrentCallInfo from "../../components/CurrentCallInfo/CurrentCallInfo";
import LocationMap from "../../components/Map/LocationMap";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

function PredicationPage() {
  return (
    <>
      <Header />
      <div className="container">
        <h1 className="page-title">לוח מחוונים לחיזוי קריאות</h1>
        <div className="cards-grid">
          <ProbabilityGauge probability={0.75} />
          <CallTypeChart
            labels={["תקלה", "תחזוקה", "חירום", "אחר"]}
            data={[45, 30, 15, 10]}
          />
          <TimePrediction hours={3} />
        </div>
        <CurrentCallInfo
          type="תקלה טכנית"
          time="14:30"
          weather="25°C, בהיר"
          specialDay="לא (יום חול רגיל)"
        />
      </div>

      <div>
        <LocationMap
          latitude={32.3161}
          longitude={34.9066}
          name="חבצלת השרון"
        />
      </div>
    </>
  );
}

export default PredicationPage;
