$(document).ready(function(){
$(".chat-send-button").click(function(){
    var msg = $(".chat-message-text").val();
    var urlmsg = encodeURIComponent(msg);
    $.getJSON('/api/'+urlmsg, function(data, jqXHR){
$(".chat-message-text").val("")
$("<div class = 'msg_user'>"+msg+"</div>").insertBefore(".reference");
$("<div class = 'msg_ai'>"+data['fields']['querry_result']+"</div>").insertBefore(".reference");
$("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
});
});
});
