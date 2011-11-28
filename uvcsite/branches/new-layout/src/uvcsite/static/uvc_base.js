$(document).ready(function()
    {

    $.tablesorter.addParser({
      id: 'germandate',
      is: function(s) {
              return false;
      },
      format: function(s) {
        var b = s.slice(0,10);
        var a = b.split('.');
        a[1] = a[1].replace(/^[0]+/g,"");
        return new Date(a.reverse().join("/")).getTime();
      },
      type: 'numeric'
    });

        $(".tablesorter").tablesorter( {widgets: ['zebra'], headers: {0: {sorter:false}, 5:{sorter:'germandate'}}});
        $("ul.tabs").tabs("div.css-panes > div");
    }
);

