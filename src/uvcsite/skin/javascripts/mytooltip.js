$(document).ready(function(){
    $("#form :input").tooltip({ 
        position: "center right", 
        offset: [-2, 10], 
        effect: "fade", 
        opacity: 0.7, 
        tip: '.tooltip' 
    });
});
