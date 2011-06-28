var shStrings = new Array();
shStrings =[{heading:"LOREM IPSUM",text:"This is an example string 1"},
	    {heading:"LOREM IPSUM",text:"This is an example string 2"},
	    {heading:"LOREM IPSUM",text:"This is an example string 3"},
	    {heading:"LOREM IPSUM",text:"This is an example string 4"},
	    {heading:"LOREM IPSUM",text:"This is an example string 5"},
	    {heading:"LOREM IPSUM",text:"This is an example string 6"},
	    {heading:"LOREM IPSUM",text:"This is an example string 7"},	    
	    {heading:"LOREM IPSUM",text:"This is an example string 8"}];
	   
var noOfStrings = shStrings.length;
	   
function showSHLine(){
	var randX=Math.floor(Math.random()*noOfStrings);	  
	$("#shString").html("<div id=\"shLHeading\">"+shStrings[randX]['heading']+"</div><div id=\"shLText\">"+shStrings[randX]['text']+"</div>");
}
window.onload = function() {
	showSHLine();
}