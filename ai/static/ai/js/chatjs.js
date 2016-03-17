$(document).ready(function(){
alert("Ddd");
$("#chat-message-text").keyup(function(event){
    if(event.keyCode == 13){
        $("#chat-send-button").click();
    }
});
var idu;
$("#chat-send-button").click(function(){
    var msg = $("#chat-message-text").val();
do{
gapi.client.load('plus','v1', function(){
 var request = gapi.client.plus.people.get({
   'userId': 'me'
 });
 request.execute(function(resp) {
   console.log('Retrieved profile for:' + resp.displayName);
idu = resp.id;
 });
});
}while(idu.length<1);
    var urlmsg = encodeURIComponent(msg);
    idu = encodeURIComponent(idu);
    $.getJSON('/api/msg='+urlmsg+'&id='+idu, function(data, jqXHR){
$("#chat-message-text").val("")
$("<div class = 'msg_user'>"+msg+"</div>").insertBefore(".reference");
$("<div class = 'msg_ai'>"+data['fields']['querry_result']+"</div>").insertBefore(".reference");
$("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
});
});
});
