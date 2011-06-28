
var arry = new Array();
arry.push("http://shaastra.org/2011/Templates_test/Media/Images/einstien.jpg|`http://www.shaastra.org");
arry.push("http://shaastra.org/2011/Templates_test/Media/Images/einstien.jpg|`www.shaastra.org");
var urls = new Array();
urls.push(arry);

//$('#back').click(
        function backclick(){
          $('#eventscontainer').slideToggle("fast",function(){});
          $('#scrollcontainer').slideToggle("slow",function(){});
        }
  //    );
$(document).ready(
    function()
    {
      
    $('#eve').click(
  
  function()
  
  {
  
        togscroll("#temporary","#scrollcontainer");       
  
  }
  
  );
  
     $('#temporary').click(
  function()
  
  {
    $('#temporary').hide();
    if(document.getElementById('scrollcontainer').style.display != "none"){
    $('#scrollcontainer').hide("slide",{direction:"down"},600);
    }
    else{
    $('#eventscontainer').hide("slide",{direction:"down"},600);
    }
  
  }
  );
     
        $('.thumbc').click(
    function()
    {
          togscroll("#temporary","#scrollcontainer"); 
              var catimg  = $(this).css("background");
              //alert(catimg);
              eventload($(this).parent().get(0).id,catimg);
                  togscroll("#temporary","#eventscontainer"); 
              
    }
);
     
    
    }   
);


function togscroll(blanket,elem){
  //alert(blanket);
  if(blanket == "#temporary"){
    $(blanket).toggle();
  }
  else{
    $(blanket).slideToggle('slow',function(){});
  }
    $(elem).slideToggle('slow',function(){});
    
}
function locate(arg,catimg){
  //alert(arg);
  window.location = arg;
}
function eventload(catid,catimg){
  //alert(catid);
  var arrcat = catid - 1;
  //alert(arrcat);
var len = urls[arrcat].length;
//alert(len);
var i = 0;
var html = new Array();
html.push("<div class = eventthumb><div id = 'back' class = 'eventthumbc' style =background:'"+catimg+"'; onclick ='javascript:backclick()'></div></div>");
//html.push(document.getElementById('escroll').innerHTML);
for(;i<len;i++){
  var url = urls[arrcat][i].split('|`');
  var imgurl = url[0];
  var linkurl = url[1];
  var id =  catid+"."+i;
  
  var attri =  "locate('"+linkurl+"');";
  var styl = "background-image:url("+imgurl+");";
  //alert(styl);
  //alert(attri);
  var code  = "<div class = eventthumb><div id = "+id+" class = 'eventthumbc' style ="+styl+" onClick="+attri+">Image</div> </div>";
  html.push(code);
  document.getElementById('escroll').innerHTML = html;
}
}