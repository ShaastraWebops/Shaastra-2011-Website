var currentUpdate2=0, length2=0, currentChar2=0, start2=0, t2=0;
var timeStep2=50, timeStepBack2=2, timeInterval2=1000;
var width2=68;

var tickerStuff2=new Array();

function getTickerData2() {

                        tickerStuff2=[{updateText:"Shaastra 2010 is over.",updateLink:"http://www.shaastra.org/2010/main/",active:"1",ticker:"1"},{updateText:"We thank all the participants for coming down to Shaastra 2010 and making it a grand success",updateLink:"http://www.shaastra.org/2010/main/",active:"1",ticker:"1"},{updateText:"We thank all the Sponsors for making Shaastra 2010 a real grand one",updateLink:"http://www.shaastra.org/2010/main/sponsorship",active:"1",ticker:"1"},{updateText:"Hope to see you at Shaastra 2011",updateLink:"http://www.shaastra.org/2010/main/",active:"1",ticker:"1"}];
			displayUpdatesInPanel2();
			type2();

}
function displayUpdatesInPanel2() {
	for (var i=0; i<tickerStuff2.length; i++) {
		if (tickerStuff2[i]['active']=='1') { 
			$('#header-updates-text ul').append("<li><a href=\"" + tickerStuff2[i]['updateLink'] + "\">"+tickerStuff2[i]['updateText']+"</a></li>");
		}
	}
	

}


function display2(str) {
	length2 = currentChar2-start2+1;
	if (length2>width2) {
		$('#ticker-link-text2').html(str.substr(length2-width2+1, currentChar2));
	}
	else {
		$('#ticker-link-text2').html(str);
	}
}

function type2() {

	if (currentChar2>=tickerStuff2[currentUpdate2]['updateText'].length) { 
		clearTimeout(t2);
		t2=setInterval("untypeNext2()", timeInterval2);
	}

	else{
		display2(tickerStuff2[currentUpdate2]['updateText'].substr(0, ++currentChar2));
		$('#ticker-link-text2').attr("href",tickerStuff2[currentUpdate2]['updateLink']);
		t2=setTimeout("type2()", timeStep2); 
	}
};

function untypeNext2() {
	display2(tickerStuff2[currentUpdate2]['updateText'].substr(0, --currentChar2));
	if (currentChar2!=0) {
		clearTimeout(t2);
		t2=setTimeout("untypeNext2()", timeStepBack2); }
	else {
		if (currentUpdate2>=tickerStuff2.length-1) {currentUpdate2=-1;} currentUpdate2++;
		type2(); 
	}
	
};
function untypePrev2() {
	display2(tickerStuff2[currentUpdate2]['updateText'].substr(0, --currentChar2));
	if (currentChar2!=0) {
		clearTimeout(t2); t2=setTimeout("untypePrev2()", timeStepBack2);  }
	else {
		if (currentUpdate2<=0) {currentUpdate2=tickerStuff2.length;} currentUpdate2--;
		type2(); 
	}
};
