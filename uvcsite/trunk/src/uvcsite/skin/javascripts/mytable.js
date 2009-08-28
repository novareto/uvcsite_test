$(document).ready(function() 
    { 
        $(".containerTable").tablesorter(
           {
               widgets: ['zebra'],
               headers: { 0: { sorter: false }} 
           }
        );
    } 
); 
