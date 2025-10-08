import { useState } from "react";
import '../Styles/Dashboard.css'
import Canvas from "./Canvas";
import SideMenu from "./SideMenu"; 
import APIEndpoint from "../APIEndpoint";

// will have a roomchooser, if room is choosed user sent to domain/rooms/12321, if room doesn't exist go back to dashboard

function Dashboard(){

    const [color,setColor] = useState("#000000ff");
    const [lineWidth,setLineWidth] = useState(2);
    const [opacity,setOpacity] = useState(1.0);

    const [curRoom, setCurRoom] = useState(-1);

    const getRooms = () => {
        
    }


    return (
        <>
            <Canvas color={color} lineWidth={lineWidth} opacity={opacity} curRoom={curRoom}/>
            <SideMenu color={color} setColor={setColor} opacity={opacity} setOpacity={setOpacity} lineWidth={lineWidth} setLineWidth={setLineWidth}/>
        </>
        )
}

export default Dashboard 