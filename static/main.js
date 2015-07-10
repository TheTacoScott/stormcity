function SetWorking()
{
  $("#fetch").fadeOut(function() {
    $("#working").fadeOut(0,function() { $(this).removeClass("hide").fadeIn(); } );
  });
}


$( document ).ready(function() {
  $("#fetchurl").click(function() { SetWorking(); });
});
