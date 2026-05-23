import React from "react";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        MyWebsite
      </div>

      <ul className="nav-links">
        <li>
          <a href="/">Home</a>
        </li>

        <li>
          <a href="/about-us">About Us</a>
        </li>

        <li>
          <a href="/contact-us">Contact Us</a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;