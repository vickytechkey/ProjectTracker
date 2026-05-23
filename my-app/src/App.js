import { BrowserRouter, Routes, Route } from "react-router-dom";
import './App.css';
import Navbar from './components/navbar/navbar';
import Footer from './components/footer/Footer';
import Login from './pages/Login';
import Home from './pages/home';

function App() {
  return (

    <>
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>


      <Footer />
    </>
  );
}

export default App;
