$(document).ready();

var flag=0;
var old_id;

function openPopUp(id,top,left){
    if(flag==1) return;
  if(flag==0){
  top=top+176;
  left=left+125;
//   $("#popup_container").fadeIn();
  var e=document.getElementById(id+"_contents");
	e.style.left=left+"px";
	e.style.top=top+"px";
	e.style.display="block";
	$("#"+id+"_contents").fadeOut(0);
	setTimeout(function(){
	$("#"+id+"_contents").animate({
	marginLeft : "-10px",
	marginTop : "-10px"
	},100);
	},201);

	setTimeout(function(){
	$("#"+id+"_contents").fadeIn(1);
	},200);
  flag=1;
  old_id="#"+id+"_contents";
  loadContents(id);
}
  else
	slide(id);
}

function closePopUp(){
  $(old_id).fadeOut();
  $("#popup_container").fadeOut();
  flag=0;
}

function loadAnimated(){
  $("#impact").animate({"width":"253px","height":"189px"},600);
}

function slide(id,top,left){
  if(flag==1){
  top=top+176;
  left=left+125;
  //   $("#"+id+"_contents").css({"z-index":"2"});
 // $(old_id).css({"z-index":"-1"}).fadeOut;;
 var e=document.getElementById(id+"_contents");
	e.style.left=left+"px";
	e.style.top=top+"px";
	e.style.display="block";
	$("#"+id+"_contents").fadeOut(0);
	setTimeout(function(){
	$("#"+id+"_contents").animate({
	marginLeft : "-10px",
	marginTop : "-10px"
	},100);
	},201);

	setTimeout(function(){
	$("#"+id+"_contents").fadeIn(1);
	},200);
  loadContents(id);
}
}
function loadContents(id){
// console.log(old_id);
 $(old_id).hide();
 // $("#"+id+"_contents").fadeIn();
  old_id="#"+id+"_contents";
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
