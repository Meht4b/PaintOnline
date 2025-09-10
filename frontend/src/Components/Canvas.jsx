import React, { useEffect } from 'react'
import socket from './Socket';

const Canvas = ({color,lineWidth,opacity}) => {
  const canvasRef = React.useRef(null);
  const [isDrawing, setIsDrawing] = React.useState(false);
  const [lastPoint, setLastPoint] = React.useState({ x: 0, y: 0 });

  

  useEffect(() => {
      const canvas = canvasRef.current;
      canvas.width = 4000;
      canvas.height = 4000;

      socket.on('draw', (data) => {
        drawStroke(data.fromX, data.fromY, data.toX, data.toY, data.lineWidth,data.color,data.opacity);
      });
      
  }, []); 

  const drawBackgroundGrid = (canvas) => {
    const ctx = canvas.getContext('2d');
    const gridSize = 20;
    ctx.strokeStyle = '#e0e0e0'; // Light gray color for grid lines
    ctx.lineWidth = 1;
    for (let x = 0; x <= canvas.width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    for (let y = 0; y <= canvas.height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
    ctx.strokeStyle = '#000000'; // Reset stroke style to black for drawing
    ctx.lineWidth = 2; // Reset line width for drawing
  }

  const drawBackgroundCheckeredPattern = (canvas) => {
    const ctx = canvas.getContext('2d');
    const patternSize = 40;
    ctx.fillStyle = '#f0f0f0';
    for (let x = 0; x < canvas.width; x += patternSize) {
      for (let y = 0; y < canvas.height; y += patternSize) {
        ctx.fillRect(x, y, patternSize / 2, patternSize / 2);
        ctx.fillRect(x + patternSize / 2, y + patternSize / 2, patternSize / 2, patternSize / 2);
      }
    }
    ctx.fillStyle = '#000000'; // Reset fill style to black for drawing
  }

  const drawBackgroundPointsPattern = (canvas) => {
    const ctx = canvas.getContext('2d');
    const pointSpacing = 20;
    ctx.fillStyle = '#d0d0d0';
    for (let x = 0; x < canvas.width; x += pointSpacing) {
      for (let y = 0; y < canvas.height; y += pointSpacing) {
        ctx.beginPath();
        ctx.arc(x, y, 1, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    ctx.fillStyle = '#000000'; // Reset fill style to black for drawing
  }
  useEffect(() => {
    const handleMouseLeave = () => {
      setIsDrawing(false);
    };
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.addEventListener('mouseleave', handleMouseLeave);
    }
    return () => {
      if (canvas) {
        canvas.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);


  const handleMouseDown = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = color ; // Use passed color prop or default
    ctx.lineWidth = lineWidth ; // Use passed lineWidth prop or default
    ctx.globalAlpha = opacity; // Set opacity (0.0 to 1.0)
    ctx.lineCap = 'flat';
    ctx.lineJoin = 'flat'; // Add this for smoother line joins
    ctx.beginPath();
    ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    setLastPoint({ x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY });
    setIsDrawing(true);
  }

  const handleMouseUp = (e) => {
    if (isDrawing){
      drawStroke(lastPoint.x, lastPoint.y, e.nativeEvent.offsetX, e.nativeEvent.offsetY);
      socket.emit('draw', {fromX: lastPoint.x, fromY: lastPoint.y, toX: e.nativeEvent.offsetX, toY: e.nativeEvent.offsetY,lineWidth:lineWidth,color:color,room:sessionStorage.getItem("user"),opacity:opacity});
    }
    setIsDrawing(false);
  }

  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (isDrawing) {
      ctx.beginPath();
      ctx.moveTo(lastPoint.x, lastPoint.y);
      ctx.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
      ctx.stroke();
      socket.emit('draw', {fromX: lastPoint.x, fromY: lastPoint.y, toX: e.nativeEvent.offsetX, toY: e.nativeEvent.offsetY, color:color,lineWidth:lineWidth,room:sessionStorage.getItem("user"),opacity:opacity});
      setLastPoint({ x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY });
    } 
  }

  const drawStroke = (fromX, fromY, toX, toY,lineWidth,otherColor,opacity) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.strokeStyle = otherColor;
    ctx.globalAlpha = opacity;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round'; // Add this for smoother line joins
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();
  }
  
  return (
      <canvas
        ref={canvasRef}
        id="canvas"
        width="800"
        height="600"
        style={{ border: 'none', touchAction: 'none' }}
        padding="0"
        margin="0"
        onMouseDown={handleMouseDown}  
        onMouseUp={handleMouseUp}
        onMouseMove={handleMouseMove}
      />
  );
}

export default Canvas
