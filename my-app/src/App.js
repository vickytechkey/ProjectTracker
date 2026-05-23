import { BrowserRouter, Routes, Route } from "react-router-dom";
import './App.css';
import Navbar from './components/navbar/navbar';
import Footer from './components/footer/Footer';
import Login from './pages/Login';
import Home from './pages/home';
import CreateProject from "./pages/CreateProject";
import CreateSubTask from "./pages/CreateSubTask";

function App() {
  return (

    <>
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create-project" element={<CreateProject />} />
          <Route path="/create-subtask" element={<CreateSubTask />} />
        </Routes>
      </BrowserRouter>


      <Footer />
    </>
  );
}

export default App;
