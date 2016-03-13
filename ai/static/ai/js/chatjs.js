$(document).ready(function(){
$("#chat-message-text").keyup(function(event){
    if(event.keyCode == 13){
        $("#chat-send-button").click();
    }
});
$("#chat-send-button").click(function(){
    var msg = $("#chat-message-text").val();
    var urlmsg = encodeURIComponent(msg);
    $.getJSON('/api/'+urlmsg, function(data, jqXHR){
$("#chat-message-text").val("")
$("<div class = 'msg_user'>"+msg+"</div>").insertBefore(".reference");
$("<div class = 'msg_ai'>"+data['fields']['querry_result']+"</div>").insertBefore(".reference");
$("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
});
});
});
