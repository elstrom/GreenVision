function playAudio() {
	document.getElementById("myAudio").play();
	document.getElementById("jeda").style="transform: translateY(-45px);";
	document.getElementById("mulai").style="opacity: 0;";
	document.getElementById("pictjeda").src="/static/Pixel/MusicOn.png";
	
} 

function pauseAudio() {
	document.getElementById("myAudio").pause();
	document.getElementById("pictmulai").src="/static/Pixel/MusicOff.png";
	document.getElementById("mulai").style="transform: translateX(0px);";
	document.getElementById("jeda").style="opacity: 0;";
}

function myFunction() {
  if (document.getElementById("topNav").className === "layout") {
    document.getElementById("topNav").className += " responsive";
  } else {
    document.getElementById("topNav").className = "layout";
  }
}