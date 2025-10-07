import { useState } from "react";
import '../Styles/Dashboard.css'
import Canvas from "./Canvas";
import SideMenu from "./SideMenu"; 

function Dashboard(){

    const [color,setColor] = useState("#000000ff");
    const [lineWidth,setLineWidth] = useState(2);
    const [opacity,setOpacity] = useState(1.0);


    return (
        <>
            <Canvas color={color} lineWidth={lineWidth} opacity={opacity}/>
            <SideMenu color={color} setColor={setColor} opacity={opacity} setOpacity={setOpacity} lineWidth={lineWidth} setLineWidth={setLineWidth}/>
        </>
        )
}

export default Dashboard 