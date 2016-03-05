$(document).ready(function(){
$(".chat-send-button").click(function(){
    var msg = $(".chat-message-text").val();
alert(msg)
    $.getJSON('/api/'+msg, function(data, jqXHR){
    // do something with response
$("<p>"+data+"</p>").insertAfter(".reference");
});
});
});
