import React from "react";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <h3>Project Tracker Application</h3>

        <ul className="footer-links">
          <li>
            <a href="/">Home</a>
          </li>

          <li>
            <a href="/create-project">Create project</a>
          </li>

          <li>
            <a href="/create-subtask">Create subtasks</a>
          </li>
        </ul>

        <p>© 2026 MyWebsite. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;