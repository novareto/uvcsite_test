$(document).ready(function() 
    { 
        $(".containerTable").tablesorter(
           {
               widgets: ['zebra'],
               headers: { 0: { sorter: false }} 
           }
        );

       $("#form-widgets-title").blur(function()
         {
          var value = $(this).val();    
          var id = $(this).attr('id')    
          console.log("input value, %s  ", value);      
          console.log("input id, %s  ", id);      
          $.getJSON('validate', 
                   {'value':value, 'id':id},
                   function(data){ console.log(data); })
         }

       );
    } 
); 
