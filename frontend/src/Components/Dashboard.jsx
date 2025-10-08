import { useEffect, useState } from "react";
import '../Styles/Dashboard.css'
import Canvas from "./Canvas";
import SideMenu from "./SideMenu"; 
import APIEndpoint from "../APIEndpoint";
import Room from "./Room.jsx"

// will have a roomchooser, if room is choosed user sent to domain/rooms/12321, if room doesn't exist go back to dashboard

function Dashboard(){

    const [color,setColor] = useState("#000000ff");
    const [lineWidth,setLineWidth] = useState(2);
    const [opacity,setOpacity] = useState(1.0);
    const [curRoom, setCurRoom] = useState(-1);
    const [roomsList,setRoomsList] = useState([])

    const getRooms = async () => {
        const url = APIEndpoint + "/get_rooms/NULLNULL"
        const options = {
            method : "GET",
            headers : {
                "Authorization" : "Bearer " + sessionStorage.getItem("token"),
                "Content-Type" : "application/json"
            }
        }
        const response = await fetch(url,options);
        const data = await response.json();
        if (response.ok){
            setRoomsList(data.rooms)
        }

    }

    useEffect(() => {
        getRooms();
    },[])


    return (
        <>
            <Canvas color={color} lineWidth={lineWidth} opacity={opacity} curRoom={curRoom}/>
            <SideMenu color={color} setColor={setColor} opacity={opacity} setOpacity={setOpacity} lineWidth={lineWidth} setLineWidth={setLineWidth}/>
            {
                roomsList.map((room,index) => (
                    <Room key={index} roomData={room}/>
                ))
            }
        </>
        )
}

export default Dashboard 