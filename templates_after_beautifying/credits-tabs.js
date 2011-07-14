var elem = new Array();
	var tabHeights = new Array();
	var noOfTabs = 1;
	var standardHeight = 320;
	
	elem = ['coreteamHeading','developersHeading'];
	
	function setHeights()	{for(i=0;i<noOfTabs;i++)	{tabHeights[i]=document.getElementById(elem[i]+'_c').offsetHeight+'px';}}
	function creditsTabsMain(e){
			document.getElementById(e).style.backgroundPosition="0px -35px";
			document.getElementById(e).style.color="#ffffff";
			for(i=0;i<noOfTabs;i++)	if(elem[i]!=e)	{document.getElementById(elem[i]).style.backgroundPosition="0px 0px"; document.getElementById(elem[i]).style.color="#183c5a";}
				
			document.getElementById(e+'_c').style.visibility="visible";
			for(i=0;i<noOfTabs;i++)	if(elem[i]!=e)	document.getElementById(elem[i]+'_c').style.visibility="hidden";
			for(i=0;i<noOfTabs;i++)	if(elem[i]!=e)	document.getElementById(elem[i]+'_c').style.height="0px"; 
			
			for(i=0;i<noOfTabs;i++){
					if(elem[i]==e){ 
							document.getElementById('jspPane').style.height=tabHeights[i]; 				
							if(parseInt(tabHeights[i])>standardHeight){
								$(function(){$('#creditsTabsContent').jScrollPane({showArrows: true,verticalScroll: true});});
							}
							else{
								$(function(){$('#creditsTabsContent').jScrollPane({showArrows: true,verticalScroll: false});});
							}
					}
			}
	}
	function showMainTab(){
		for(i=0;i<noOfTabs;i++)	{
						document.getElementById(elem[i]).style.backgroundPosition="0px 0px"; 
						document.getElementById(elem[i]).style.color="#183c5a";
						document.getElementById(elem[i]+'_c').style.visibility="hidden";
						document.getElementById(elem[i]+'_c').style.height="0px"; 
				}
				document.getElementById('creditsMainContent').style.visibility="visible";
	}
	window.onload = function(){
		setHeights();
		document.getElementById(elem[0]).style.backgroundPosition="0px -35px";
		document.getElementById(elem[0]).style.color="#ffffff";
		hospiTabsMain(elem[0]);
		
		$("#creditsContainer").css('visibility','visible');
		$("#creditsContainer").fadeOut(0).fadeIn(1500);
	}
	$(document).ready(function(){
		$("#creditsTabs").click(function(e){
			var id = e.target.id;
			hospiTabsMain(id);
		});
		$(function(){
			$('#creditsTabsContent').jScrollPane({showArrows: true,verticalScroll: true});
		});
	});
