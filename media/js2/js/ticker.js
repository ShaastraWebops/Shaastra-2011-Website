var currentUpdate=0, length=0, currentChar=0, start=0, t=0;
var timeStep=50, timeStepBack=2, timeInterval=1000;
if (screen.width<=1024)
     var width=67;
else var width=81;

var tickerStuff=new Array();

function getTickerData() {

                        tickerStuff=[{updateText:"Shaastra 2011 Site is Up.",updateLink:"http://www.shaastra.org/2011/landing/",active:"1",ticker:"1"},{updateText:"Shaastra 2010 is over.",updateLink:"http://www.shaastra.org/2010/main/",active:"1",ticker:"1"},{updateText:"We thank all the participants for coming down to Shaastra 2010 and making it a grand success",updateLink:"http://www.shaastra.org/2010/main/",active:"1",ticker:"1"},{updateText:"We thank all the Sponsors for making Shaastra 2010 a real grand one",updateLink:"http://www.shaastra.org/2010/main/sponsorship",active:"1",ticker:"1"},{updateText:"Hope to see you at Shaastra 2011",updateLink:"http://www.shaastra.org/2010/main/",active:"1",ticker:"1"}];
			displayUpdatesInPanel();
			type();

}
function displayUpdatesInPanel() {
	$('#header-updates-text').html("");
	$('#header-updates-text').append("<ul></ul>");
	for (var i=0; i<tickerStuff.length; i++) {
		if (tickerStuff[i]['active']=='1') { 
			$('#header-updates-text ul').append("<li><a href=\"" + tickerStuff[i]['updateLink'] + "\">"+tickerStuff[i]['updateText']+"</a></li>");
		}
	}
	

}


function display(str) {
	length = currentChar-start+1;
	if (length>width) {
		$('#ticker-link-text').html(str.substr(length-width+1, currentChar));
	}
	else {
		$('#ticker-link-text').html(str);
	}
}

function type() {

	if (currentChar>=tickerStuff[currentUpdate]['updateText'].length) { 
		clearTimeout(t);
		t=setInterval("untypeNext()", timeInterval);
	}

	else{
		display(tickerStuff[currentUpdate]['updateText'].substr(0, ++currentChar));
		$('#ticker-link-text').attr("href",tickerStuff[currentUpdate]['updateLink']);
		t=setTimeout("type()", timeStep); 
	}
};

function untypeNext() {
	display(tickerStuff[currentUpdate]['updateText'].substr(0, --currentChar));
	if (currentChar!=0) {
		clearTimeout(t);
		t=setTimeout("untypeNext()", timeStepBack); }
	else {
		if (currentUpdate>=tickerStuff.length-1) {currentUpdate=-1;} currentUpdate++;
		type(); 
	}
	
};
function untypePrev() {
	display(tickerStuff[currentUpdate]['updateText'].substr(0, --currentChar));
	if (currentChar!=0) {
		clearTimeout(t); t=setTimeout("untypePrev()", timeStepBack);  }
	else {
		if (currentUpdate<=0) {currentUpdate=tickerStuff.length;} currentUpdate--;
		type(); 
	}
};