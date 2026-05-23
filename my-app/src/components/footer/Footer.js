import React from "react";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <h3>MyWebsite</h3>

        <ul className="footer-links">
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

        <p>© 2026 MyWebsite. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;