$(document).ready(function()
    {
        $(".tablesorter").tablesorter( {widgets: ['zebra'], headers: {0: {sorter:false}}});

/*

        $.each($('div.row'), function() {
            var description = $(this).children('label').children('span.small').text();
            $(this).children('div.widget').children('input').attr('title', description);
            $(this).children('label').children('span.small').hide();
        });

*/

        $("form :input").tooltip({ 
            position: "center right", 
            offset: [-2, 10], 
            effect: "fade", 
            opacity: 0.7, 
            tip: '.tooltip',
        });

        $("ul.tabs").tabs("div.css-panes > div");
    }
);

