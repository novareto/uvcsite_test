$(document).ready(function(){
    $("p#ubl").click(function(){
	$(this).next().slideToggle('slow');
    });

	$("#tabs").tabs();

});
