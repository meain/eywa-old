$(document).ready(function(){
$("#chat-message-text").keyup(function(event){
    if(event.keyCode == 13){
        $("#chat-send-button").click();
    }
});
$("#chat-send-button").click(function(){
alert("lskdjf")
    var msg = $("#chat-message-text").val();
    var urlmsg = encodeURIComponent(msg);
    $.getJSON('/api/'+urlmsg, function(data, jqXHR){
$("#chat-message-text").val("")
$("<div class = 'msg_user'>"+msg+"</div>").insertBefore(".reference");
$("<div class = 'msg_ai'>"+data['fields']['querry_result']+"</div>").insertBefore(".reference");
$("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
});
});
$("#signinButton").click(
function(){alert("ddd")}
);
function signinCallback(authResult) {
  if (authResult['access_token']) {
alert("aay")
    // Successfully authorized
    document.getElementById('signinButton').setAttribute('style', 'display: none');
gapi.client.load('plus','v1', function(){ 
// once we get this call back, gapi.client.plus.* will exist
});
    profile: function(){
      gapi.client.plus.people.get({
        'userId': 'me'
      }).then(function(res) {
        var profile = res.result;
        console.log(profile);
        $('#profile').empty();
        $('#profile').append(
            $('<p><img src=\"' + profile.image.url + '\"></p>'));
        $('#userid').empty();
        $('#userid').append(
            $(profile.id)
        );
      }, function(err) {
        var error = err.result;
        $('#profile').empty();
        $('#profile').append(error.message);
      });
    }
  };
  } else if (authResult['error']) {
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatially log in the user
    // console.log('There was an error: ' + authResult['error']);
  }
}


function disconnectUser(access_token) {
  var revokeUrl = 'https://accounts.google.com/o/oauth2/revoke?token=' +
      access_token;

  // Perform an asynchronous GET request.
  $.ajax({
    type: 'GET',
    url: revokeUrl,
    async: false,
    contentType: "application/json",
    dataType: 'jsonp',
    success: function(nullResponse) {
      // Do something now that user is disconnected
      // The response is always undefined.
    },
    error: function(e) {
      // Handle the error
      // console.log(e);
      // You could point users to manually disconnect if unsuccessful
      // https://plus.google.com/apps
    }
  });
}
// Could trigger the disconnect on a button click
$('#revokeButton').click(disconnectUser);
