$(document).ready();

var flag=0;
var old_id;

function openPopUp(id,top,left,width,height){
  if(flag==0){
  top=top+176;
  left=left+125;
//   $("#popup_bg").fadeIn();
  var bg="url(\"http://www.shaastra.org/2011/media/main/img/"+id+"_copy.png\")";
  $("#popup_container").css({"width":width,"height":height,"background":bg});
  var e=document.getElementById("popup_container");
	e.style.left=left+"px";
	e.style.top=top+"px";
	e.style.display="block";
	$("#popup_container").fadeOut(0);
	setTimeout(function(){
	$("#popup_container").animate({
	marginLeft : "-10px",
	marginTop : "-10px"
	},100);
	},201);

	setTimeout(function(){
	$("#popup_container").fadeIn(1);
	},200);
  flag=1;
  old_id="#"+id+"_contents";
$(old_id).hide();
  old_id="#"+id+"_contents";
  load_contents(id);
}
  else
	slide(id);
}

function closePopUp(){
  $(old_id).hide();
  $("#popup_container").fadeOut();
  flag=0;
}

function loadAnimated(){
  $("#impact").animate({"width":"253px","height":"189px"},600);
}

function slide(id,top,left,width,height){
  if(flag==1){
  top=top+176;
  left=left+125;
  var bg="url(\"http://www.shaastra.org/2011/media/main/img/"+id+"_copy.png\")";
  $("#popup_container").stop().css({"width":width,"height":height,"background":bg});
  var e=document.getElementById("popup_container");
	e.style.left=left+"px";
	e.style.top=top+"px";
	e.style.display="block";
	$("#popup_container").fadeOut(0);
	setTimeout(function(){
	$("#popup_container").animate({
	marginLeft : "-10px",
	marginTop : "-10px"
	},100);
	},201);

	setTimeout(function(){
	$("#popup_container").fadeIn(1);
	},200);
$(old_id).hide();
  old_id="#"+id+"_contents";
  load_contents(id);
}
}

function load_popup(){
  $("#footer_container").css({"position":"absolute","top":"598px"});
  $("body").css({"overflow":"hidden"});
  $("#content").animate({"left":"-1200px"},600);
  $("#container1").show().animate({"left":"125px"},600);
//   $("#content").hide();
  $("#right_arrow").fadeOut();
  $("#left_arrow").fadeIn();
  $("#content").fadeOut();
  setTimeout(function(){$("body").css({"overflow":"auto"});},600);
}

function close_popup(){
  closePopUp();
    $("#footer_container").css({"position":"relative","top":"0px"});
  $("body").css({"overflow":"hidden"});
  $("#content").show().animate({"left":"0px"},600);
  $("#container1").animate({"left":"1200px"},600).fadeOut();
  $("#right_arrow").fadeIn();
  $("#left_arrow").fadeOut();
  setTimeout(function(){$("body").css({"overflow":"auto"});},1000);
}

function load_contents(id){
  $("#"+id+"_contents").fadeIn();
}


function preloadimages(arr){
	var newimages=[]
	var arr=(typeof arr!="object")? [arr] : arr //force arr parameter to always be an array
	for (var i=0; i<arr.length; i++){
		newimages[i]=new Image()
		newimages[i].src=arr[i]
	}
	$("#right_arrow").fadeIn();
}

function loading(){
preloadimages(['http://www.shaastra.org/2011/media/main/img/aerofest.jpg','http://www.shaastra.org/2011/media/main/img/aerofest_copy.png','http://www.shaastra.org/2011/media/main/img/coding.jpg','http://www.shaastra.org/2011/media/main/img/coding_copy.png','http://www.shaastra.org/2011/media/main/img/design_and_build.jpg','http://www.shaastra.org/2011/media/main/img/design_and_build_copy.png','http://www.shaastra.org/2011/media/main/img/exhibitions.jpg','http://www.shaastra.org/2011/media/main/img/exhibitions_copy.png','http://www.shaastra.org/2011/media/main/img/flagship.jpg','http://www.shaastra.org/2011/media/main/img/flagship_copy.png','http://www.shaastra.org/2011/media/main/img/impact.jpg','http://www.shaastra.org/2011/media/main/img/impact_copy.png','http://www.shaastra.org/2011/media/main/img/involve.jpg','http://www.shaastra.org/2011/media/main/img/involve_copy.png','http://www.shaastra.org/2011/media/main/img/online.jpg','http://www.shaastra.org/2011/media/main/img/online_copy.png','http://www.shaastra.org/2011/media/main/img/quizzes.jpg','http://www.shaastra.org/2011/media/main/img/quizzes_copy.png','http://www.shaastra.org/2011/media/main/img/soe.jpg','http://www.shaastra.org/2011/media/main/img/soe_copy.png','http://www.shaastra.org/2011/media/main/img/spotlights.jpg','http://www.shaastra.org/2011/media/main/img/spotlights_copy.png' ,'http://www.shaastra.org/2011/media/main/img/workshops.jpg','http://www.shaastra.org/2011/media/main/img/workshops_copy.png']);
}
