$(document).ready(function()
    {
      $('input#form-action-senden-mit-ajax').click(function(event) {
          var data = 'KLAUS';
          var uri = window.location;
          $.getJSON(uri+'/@@getData', data, function(data) {
                $('div#above-page').append(data);
              }) 
          event.preventDefault();
          $('form :input').first().focus();
      });
    }
)
    
