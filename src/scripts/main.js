var colors = ["blue", "red", "green", "pink"];
var x = 0;

var int  = setInterval(function() {
	document.body.style.backgroundColor = colors[x%5];
	x++;
}, 500);