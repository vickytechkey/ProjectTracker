import React from "react";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        Project Tracker Application
      </div>

      <ul className="nav-links">
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
    </nav>
  );
}

export default Navbar;