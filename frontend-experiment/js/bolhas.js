var canvas = document.getElementById('ondas');
setCanvas();

function setCanvas(){
  if (canvas.getContext){
    ctx = canvas.getContext("2d");
  }
}
