		
			var tabWidth =new Array();
			var totalWidth=0;
			var totalWidthRow2=0;
			var multiplier=12;
			var standardWidth=776;
			var standardHeight=260;			
			
			function modUserContent(){
			var d_=0;
				for(d_=0;d_<noOfTabs;d_++){
					document.getElementById(elem[d_]).innerHTML=document.getElementById(elem[d_]).innerHTML.replace(/font-family/g,"NA");	
					document.getElementById(elem[d_]).innerHTML=document.getElementById(elem[d_]).innerHTML.replace(/<br>/g,"");
				}
			}
			for(x=0;x<noOfTabs;x++){
				tabWidth[x]=multiplier*tabNames[x].length+'px';
				totalWidth+=parseInt(tabWidth[x]);
				
				if(totalWidth>standardWidth) {totalWidth-=parseInt(tabWidth[x]); setCorrectWidth(totalWidth,x,0);  prepareNextRow(x);	break;}	
			}
			
			if(totalWidth<=standardWidth && totalWidthRow2==0) setCorrectWidth(totalWidth,noOfTabs,0);
			
			function setCorrectWidth(w,n,index){			//width,no of tabs in one row less one,index of the tab where to start setting width from
				var delta=standardWidth-w;
				var increment=delta/n;
				for(x=index;x<index+n;x++){
					tabWidth[x]=parseInt(tabWidth[x])+increment+'px';	
					//alert(tabWidth[x]);
				}
			}
			
			function prepareNextRow(x){			//no of tabs in the previous row less one
				for(s=x;s<noOfTabs;s++){
					tabWidth[s]=multiplier*tabNames[s].length+'px';
					totalWidthRow2+=parseInt(tabWidth[s]);
					
				}
				//alert(totalWidthRow2);
				if(totalWidthRow2>standardWidth) {}	
				if(totalWidthRow2<=standardWidth) {setCorrectWidth(totalWidthRow2,noOfTabs - x,x);}			
			}
			
			
			
			
			
			var tabHeights=new Array();
			
			$(function(){
				modUserContent();
				$('#event-details').jScrollPane({showArrows: true,verticalScroll: true});
			});
			window.onload=function(){
				if(elem[0]!=null){		
					setHeights();				
					setVisible(elem[0]);
					setBgGreen(elem[0]);
				}	
			}

			$(document).ready(function(){		
				/*var oht=document.getElementById('content').offsetHeight;
				var ht;
				$("#page").mouseover(function(){
					ht=$(window).height();
					//$("#asdf_").text("Height : "+$(window).height());
					if(ht>600||oht<420){
						$("#content").css({'height':ht-208+'px'});
						}
					else{
						$("#content").css({'height':oht+'px'});
					}
				});	*/
				
			
				if(IntExp){
					$("#event-details").css('marginTop',00);
					//document.getElementById('event-details').style.marginTop="-40px";
				}
				for(x=0;x<noOfTabs;x++){
					document.getElementById(elem[x]).style.width=tabWidth[x];
				}
			if(totalWidth<=standardWidth && totalWidthRow2==0){
				//$("#tabs").css({'height' :'40px','top' :'00px'});	
				//$("#eventsTab").css({'height':'360px','background-image' :'url(http://shaastra.org/2011/media/main/img/contentBox_.png)','background-position' :'0px 00px','padding-top':'-40px'});
				//$("#event-details").css('marginTop',-40);
				$("#tabs").css({'height' :'40px','top' :'40px'});	
				$("#eventsTab").css({'background-image' :'url(http://shaastra.org/2011/media/main/img/contentBox_.png)','background-position' :'0px 40px','margin-top':'-40px'});
				//$("#event-details").css('marginTop',-40);
				}
			if(totalWidthRow2>0){
				$("eventsTab").css({'margin-top':'-40px'});
			}
				
			
				$("#tabs").click(function(e) {
					var id=e.target.id;
					//alert(id);
					setBgGreen(id);
					setVisible(id);							
				});	
				
				
				/*$("#Question2").click(function(e) {
					setHeights();
					$('#event-details').jScrollPane({showArrows: true,verticalScroll: true});
					var id=e.target.id;
					setBgGreen(id);
					setVisible(id);							
				});*/
				
				$("#ticker2").css('display','none');	
			});
			
			function setVisible(e){
				document.getElementById(e+'_').style.visibility="visible";
				
				for(i=0;i<noOfTabs;i++)	if(elem[i]!=e)	document.getElementById(elem[i]+'_').style.visibility="hidden";
				for(i=0;i<noOfTabs;i++)	if(elem[i]!=e)	document.getElementById(elem[i]+'_').style.height="0px"; 
				for(i=0;i<noOfTabs;i++){
									if(elem[i]==e){
											document.getElementById('jspPane').style.height=tabHeights[i]; 				
											if(parseInt(tabHeights[i])>standardHeight){
												$("#event-details").css('padding-left','3px');	
												$(function(){$('#event-details').jScrollPane({showArrows: true,verticalScroll: true});});
											}
											else{
												$("#event-details").css('padding-left',"1px");		// '13px' <=> '8px'
												$(function(){$('#event-details').jScrollPane({showArrows: true,verticalScroll: false});});
											}
									}
								}
				
			}
			
			function setBgGreen(e){
				document.getElementById(e).style.backgroundColor="#93C66E";
				for(i=0;i<noOfTabs;i++)	if(elem[i]!=e)	document.getElementById(elem[i]).style.backgroundColor="#5185BE";
			}
			
			function setHeights(){				
				for(i=0;i<noOfTabs;i++){
									tabHeights[i]=document.getElementById(elem[i]+'_').offsetHeight+'px';
				}
			}