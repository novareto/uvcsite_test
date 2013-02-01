$(function() {
    var form = $("div#page-body").click(function() {
        $(this).expose({
             loadSpeed: 'normal',
             opacity: 0.8,
             color: 'grey',
             onLoad: function() { form.css({'border': '2px solid #B30B16',}); },
             onClose: function() { form.css({'border-color': '#DDDDDD'}); },
        });
    });
});
