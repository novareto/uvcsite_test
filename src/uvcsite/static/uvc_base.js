$(document).ready(function()
    {
        $(".tablesorter").tablesorter( {widgets: ['zebra'], headers: {0: {sorter:false}}});

        $("#form :input").tooltip({ 
            position: "center right", 
            offset: [-2, 10], 
            effect: "fade", 
            opacity: 0.7, 
            tip: '.tooltip' 
        });
    }
);

