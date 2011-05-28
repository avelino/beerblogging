/*
 * ondas v1.0
 * Copyright 2010 John Pezzetti
 * By John Pezzetti of http://www.otherhalffull.com
 * 
 * If you want to use this script, links to http://www.otherhalffull.com are always appreciated
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
 
//Settings -- feel free to change these values
var totalPoints = 13; //Total # of Peaks & Valleys. Should be an odd number to account for the middle point.
var ampMultiplier = .3; //Amplitude of the waves. Further multipled by totalPoints.
var framerate = 30; //framerate in ms (1000/30 = 33.33 fps)
var cWidth = 960; //Canvas Width will be changed to the width of the viewport
var cHeight = 250; //Canvas Height
var waterLevel = 200; //The y value of the surface of the water
var spreadAccelleration = 1.01; //Acceleration for point spread
var spreadSpeed = 20; //Fixed speed for point spread

//Global Static Variables
var dur = (totalPoints-3)*9; //Duration. Calculation is Total points, minus mid and end points
var midPointIndex = Math.floor(totalPoints/2); //The index of the midpoint within the Points array
var midPointX; //X position of cursor
var canvas; //The canvas element
var ctx; //The Canvas Context
var animation; //Interval that runs drawing script
var animationActive = false; //true when an animation is occuring, used to control the frequency of the animation
var C = Math.PI/180; //Constant used in the sine function
var points; //An array container that holds each point
var point; //Holds the current point
var counter; //The counter that we'll increment to control each frame of the animation

//If not using jQuery you'll have to replace parts of this code, namely the hover control
$(document).ready(function() {
  $('#ondas').hover(function(e){
    if (canvas.getContext){
      if (!animationActive){
        clearInterval(animation);
        midPointIndex = Math.floor(totalPoints / 2);
        midPointX = e.pageX;
        point = 1; //Start counting at 1 since we're setting points[0] at the get go
        counter = 0;
        points = new Array();
        points[0] = new Array(spreadSpeed,0);//The outer points ground out the mid point
        animation = setInterval(drawShape, framerate); 
        animationActive = true;
      }
    }
  });
  
  canvas = document.getElementById('ondas');
  setCanvas();
  
  $(window).resize(function() {
    setCanvas();
  });      
});

//Initialize the canvas for supporting browsers
function setCanvas(){
$("#ondas").attr('width',viewportWidth)
  if (canvas.getContext){//Check that canvas element will fire  
    var viewportWidth = $('body').width();
    $("#ondas").attr('width',viewportWidth).attr('height',cHeight);
    cWidth = viewportWidth;   
    ctx = canvas.getContext("2d");
    var gradient = ctx.createLinearGradient(0, 0, 0, 1000);
	gradient.addColorStop(0, "white");
	gradient.addColorStop(1, "black");
	ctx.fillStyle = gradient;
    drawSquare();  
  }
}

function stopAni(){
  clearInterval(animation);
}
 
//Draw the initial static water shape
function drawSquare(){
  ctx.fillRect(0,0,cWidth,waterLevel);
  $("#trailing-header").css("height","60px");
}  
  
function drawShape(){
   
  midPointY = Math.sin(counter*10*C)*((dur-counter)*ampMultiplier); //Calculates the y value of the midpoint

  if (counter <= dur){
    points[midPointIndex] = new Array(0,midPointY);
    
    //Check if counter has reached 90deg or 270deg, if so, time to spawn another point
    if (counter%9 == 0 && counter%2 == 1){
      points[point] = Array(-1,midPointY);
      point++;
    }
  }
  
  ctx.clearRect(0,0,canvas.width,canvas.height); //Clear the canvas

  ctx.beginPath();
  ctx.moveTo(0, waterLevel); //Start on the left side
  
  //Will contain the previous point to help each point set its bezier curve
  var lastPoint = new Array(0,waterLevel);
  
  //Loop through the array of points
  //Calculates the proper x and y values of each point
  //Does the actual drawing
  for (var pt = 0; pt < totalPoints; pt++){
    if (points[pt]){
      if (pt < midPointIndex){
        points[pt][0] = (points[pt][0]*spreadAccelleration)-spreadSpeed; //Move points away from the center point
        points[(midPointIndex-pt)+midPointIndex] = new Array(-points[pt][0],points[pt][1]); //Create an opposite point
      }
      
      var x = points[pt][0]+midPointX;
      var y = points[pt][1]+waterLevel;
      
      var bezHandle1 = ((x-lastPoint[0])/2)+lastPoint[0];
      var bezHandle2 = x-((x-lastPoint[0])/2);
      ctx.bezierCurveTo(bezHandle1, lastPoint[1], bezHandle2, y, x, y);
      
      lastPoint[0] = x;
      lastPoint[1] = y;
    }
  };
  
  
  //The Water Level has been rendered, draw the rest of the container
  ctx.lineTo(cWidth, waterLevel);
  ctx.lineTo(cWidth, 0);
  ctx.lineTo(0,0);
  ctx.closePath();
  
  ctx.fill();
  
  counter++;
  if ( counter == dur) animationActive = false;
  if (counter >= (dur*z)) stopAni();          

} 
