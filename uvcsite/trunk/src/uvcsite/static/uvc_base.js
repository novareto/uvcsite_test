$(document).ready(function()
    {
        $(".tablesorter").tablesorter( {widgets: ['zebra'], headers: {0: {sorter:false}}});

        $("ul.tabs").tabs("div.css-panes > div");
    }
);

