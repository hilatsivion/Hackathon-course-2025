import React from "react";
import "./Header.css";
import emekLogo from "../../assets/images/emek-logo.png";

function Header() {
  return (
    <header className="header">
      <img src={emekLogo} alt="עמק חפר לוגו" className="header-logo" />
    </header>
  );
}

export default Header;
