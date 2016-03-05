$(document).ready(function(){
$(".chat-send-button").click(function(){
    var msg = $(".chat-message-text").val();
    $.getJSON('/api/'+msg, function(data, jqXHR){
    // do something with response
$(".chat-message-text").val("")
$("<div class = 'msg_user'>"+msg+"</div>").insertBefore(".reference");
$("<div class = 'msg_ai'>"+data['fields']['querry_result']+"</div>").insertBefore(".reference");
});
});
});
