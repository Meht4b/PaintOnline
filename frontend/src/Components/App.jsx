import { useEffect, useState } from 'react'
import '../Styles/App.css'
import Canvas from './Canvas'
import Login from './Login'
import socket from './Socket'
import SideMenu from './SideMenu'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard.jsx'; // the post-login component
import LandingPage from './LandingPage.jsx';

function App() {

  

  useEffect(() => {
      socket.on("user_joined", (data) => {
        console.log(data.message);
      });
      socket.on("connect", () => {
        console.log("Connected to socket server");
      });
  }, []);
  const [loggedIn, setLoggedIn] = useState(false);
  
  const callbackFunction = () => {
    socket.emit("join_canvas", {"user_name":sessionStorage.getItem("user")});
  }

return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage loggedIn ={loggedIn} />} />
        <Route path="/login" element={<Login propLogin={1} propError={0} setLoggedIn={setLoggedIn} callBack={callbackFunction}/>}/>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App
