import { useEffect, useState } from 'react'
import '../Styles/App.css'
import Canvas from './Canvas'
import Login from './Login'
import socket from './Socket'
import SideMenu from './SideMenu'


function App() {

  const [color,setColor] = useState("#000000ff");
  const [lineWidth,setLineWidth] = useState(2);
  const [opacity,setOpacity] = useState(1.0);

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
    <>
      {
        loggedIn ?
        <>
        <Canvas color={color} lineWidth={lineWidth} opacity={opacity}/>
        <SideMenu color={color} setColor={setColor} opacity={opacity} setOpacity={setOpacity} lineWidth={lineWidth} setLineWidth={setLineWidth}/>
        </>
         : 
        <Login propLogin={1} propError={0} setLoggedIn={setLoggedIn} callBack={callbackFunction} />
      }
    </>
  )
}

export default App
