import logo from './logo.svg';
import './App.css';
import Navbar from './components/navbar/navbar';
import Footer from './components/footer/Footer';

function App() {
  return (
   <>
     

      <Navbar />

      <div className="content">
        <h1 style={{color:"white"}}>
          Welcome
        </h1>
      </div>

      <Footer />
    </>
  );
}

export default App;
