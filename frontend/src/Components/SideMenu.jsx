import React from 'react'
import '../Styles/SideMenu.css'

const SideMenu = ({color,setColor,opacity,setOpacity,lineWidth,setLineWidth}) => {

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
  <>    
  <div className='side-menu-cont'>
      <div className='side-menu-item-cont'>
        <h3>Color</h3> 
        <div className='color-picker-outer-cont'>
          <div className='color-picker-input-cont'>
            <input type="color" value={color} onChange={(e) => setColor(e.target.value)} />
            <div className='color-picker-display' style={{backgroundColor: color,width:"100%",height:"100%"}} ></div>
          </div>
          <div className='color-picker-text-cont'>
            <input type="text" id='color-input-text'value={color} onChange={(e) => setColor(e.target.value)} />
            <input type="text" id='opacity-input-text' value={opacity} onMouseDown={handleOpacityDrag} onChange={(e)=>{if (e.target.value>=0 && e.target.value<=1) setOpacity(e.target.value)}} />
          </div>
        </div>

      </div>
      <div className='side-menu-item-cont'>
        <h3>Thickness</h3>
        <input type="range" min="1" max="20" value={lineWidth} onChange={(e) => setLineWidth(e.target.value)} className='line-width-slider' />
      </div>

  </div>
 
  </>
 )
}

export default SideMenu
