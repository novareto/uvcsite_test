$(document).ready(function()
    {

        $.each($('div.row'), function() {
            var description = $(this).children('label').children('span.small').text();
            if (description != '') { 
                $(this).children('div.widget').children('input').attr('title', description).attr('tooltip','1');
                $(this).children('label').children('span.small').hide();
            }
            else {
                $(this).children('div.widget').children('input').attr('title', '0');
            }
        });


        $("form :input[tooltip='1']").not(":button").tooltip({ 
            position: "center right", 
            offset: [-2, 10], 
            effect: "fade", 
            opacity: 0.8, 
            tip: '.tooltip',
        });

    }
);

