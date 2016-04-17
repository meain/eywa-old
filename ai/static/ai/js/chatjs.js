function isEmptyOrSpaces(str){
    return str === null || str.match(/^ *$/) !== null;
}

$(document).ready(function(){
var idu;
$('#chat-message-text').click(function () {
document.getElementById("user-profile").src = "../static/ai/img/profile.png";
gapi.client.load('plus','v1', function(){
 var request = gapi.client.plus.people.get({
   'userId': 'me'
 });
 request.execute(function(resp) {
   console.log('Retrieved profile for:' + resp.displayName + ' ' + resp.image.url);
idu = resp;
if(resp.image.url!='undefined'){
    document.getElementById("user-profile").src = resp.image.url;
}
 });
});
});
$('#signinmodal').on('hidden.bs.modal', function () {
document.getElementById("user-profile").src = "../static/ai/img/profile.png";
gapi.client.load('plus','v1', function(){
 var request = gapi.client.plus.people.get({
   'userId': 'me'
 });
 request.execute(function(resp) {
   console.log('Retrieved profile for:' + resp.displayName + ' ' + resp.image.url);
if(resp.image.url!='undefined'){
    document.getElementById("user-profile").src = resp.image.url;
}
 });
});
})
$("#signout").click(
function logout()
{
    gapi.auth.signOut();
    //location.reload();
gapi.client.load('plus','v1', function(){
 var request = gapi.client.plus.people.get({
   'userId': 'me'
 });
 request.execute(function(resp) {
   console.log('Retrieved profile for:' + resp.displayName);
idu = resp;
 });
});
}
);
$("#chat-message-text").keyup(function(event){
    if(event.keyCode == 13){
        $("#chat-send-button").click();
    }
});
$("#chat-send-button").click(function(){
    var msg = $("#chat-message-text").val();
    if(!isEmptyOrSpaces(msg)){

gapi.client.load('plus','v1', function(){
 var request = gapi.client.plus.people.get({
   'userId': 'me'
 });

 request.execute(function(resp) {
   console.log('Retrieved profile for:' + resp.displayName);
idu = resp;
 });
});
    var urlmsg = encodeURIComponent(msg);
    idu = JSON.stringify(idu);
    idu = encodeURIComponent(idu);
    $.getJSON('/api/msg='+urlmsg+'&id='+idu, function(data, jqXHR){
$("#chat-message-text").val("")
$("<div class = 'msg_user'>"+msg+"</div>").insertBefore(".reference");
$("<div class = 'msg_ai'>"+data['fields']['querry_result']+"</div>").insertBefore(".reference");
$("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
});
}
});
});
