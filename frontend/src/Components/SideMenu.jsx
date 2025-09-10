import React from 'react'
import '../Styles/SideMenu.css'

const SideMenu = ({color,setColor,opacity,setOpacity}) => {

  // Helper to handle drag for opacity
  const handleOpacityDrag = (e) => {
    let startX = e.clientX;
    let startOpacity = parseFloat(opacity);

    const onMouseMove = (moveEvent) => {
      const deltaX = moveEvent.clientX - startX;
      // Change opacity by 0.01 per 5px dragged
      let newOpacity = Math.min(1, Math.max(0, startOpacity + deltaX * 0.01));
      setOpacity(newOpacity.toFixed(2));
    };

    const onMouseUp = () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  };

  return (
    <div className='sidemenu-cont'>
      <h3>color</h3>
      <div className='color-cont sidemenu-item'>
        <div className='color-picker-cont'>
        <div className='color-display'
        style={{ backgroundColor: color, width: '100%', height: '100%', position: 'absolute', top: 0, left: 0 }}
        >

        </div>
        <input
          id="colorPicker"
          type="color"
          className='colorPicker'
          value={color}
          onChange={e => setColor(e.target.value)}
        />

 
        </div> 
       <div className='color-text-cont'>
        <input id='color' type="text" value={color} onChange={(e)=>{setColor(e.target.value)}} />
        <input id='opacity-picker'
          type="text"
          value={opacity}
          onChange={(e) => {if (e.target.value<=1 && e.target.value >= 0) setOpacity(e.target.value)}}
          onMouseDown={handleOpacityDrag}
          style={{ cursor: 'ew-resize' }}
          draggable="false"
          
        />
 
        </div>
     </div>
   </div>
  )
}

export default SideMenu
