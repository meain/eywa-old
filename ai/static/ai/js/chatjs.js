var gId = '';
var gName = '';
var gImage = '';
var gEmail = '';
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId());
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail());
    //Save data
    gId = profile.getId();
    gName = profile.getName();
    gImage = profile.getImageUrl();
    gEmail = profile.getEmail();
    showSignInOrImg();
}
function checkIfSignedIn(){
    if (gId != ''){return true;
    }
    else{return false;
        console.log("User not signed in");
    }
}
function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
        gId = '';
        gName = '';
        gImage = '';
        gEmail = '';
        showSignInOrImg();
    });
}
function showSignInOrImg(){
    if (checkIfSignedIn()){
        $("#user-profile")[0].style.display = "inline";
        $(".gsignin")[0].style.display = "none";
        $("#user-name")[0].style.display = "inline-block";
        $("#user-name")[0].innerHTML = gName;
        if(gImage.indexOf("http") > -1){
            $("#user-profile")[0].src = gImage
        }
    }
    else{
        $(".gsignin")[0].style.display = "inline";
        $("#user-name")[0].style.display = "none";
        $("#user-profile")[0].style.display = "none";
        $("#user-name")[0].innerHTML = "";
    }
}
function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}
//So that scroll can be adjusted
function getImageSize(img, callback) {
    var $img = $(img);

    var wait = setInterval(function() {
        var w = $img[0].naturalWidth,
        h = $img[0].naturalHeight;
        if (w && h) {
            clearInterval(wait);
            callback.apply(this, [w, h]);
        }
    }, 30);
}
//Funciton to do animaiton
$.fn.extend({
  animateCss : function(animationName){
    var animationEnd = 'webkitAnimationEnd onanimationend animationend' ;
    $(this).addClass('animated ' + animationName).one(animationEnd, function(){
        $(this).removeClass('animated ' + animationName);
    });
  }
});
$(document).ready(function() {
    $("#chat-message-text").focus();
    showSignInOrImg();
    var idu;
    $("#user-profile").click(function(){
        signOut();
    });
    $("#user-profile").hover(
        function(e){
            $("#user-profile")[0].src = "../static/ai/img/signout.png"
            $("#user-name")[0].innerHTML = "Sign Out";
        },
        function(e){
            $("#user-profile")[0].src = gImage
            $("#user-name")[0].innerHTML = gName;
        }
    );
    $("#chat-message-text").keyup(function(event) {
        if (event.keyCode == 13) {
            $("#chat-send-button").click();
        }
    });
    $("#chat-send-button").click(function() {
        var msg = $("#chat-message-text").val();
        if (!isEmptyOrSpaces(msg)) {
            $("#chat-message-text").val("")
            $("<div class = 'msg_user animated slideInRight'>" + msg + "</div>").insertBefore(".reference");
            $("#chat-msg-box").stop();
            $("#chat-msg-box").animate({scrollTop:$("#chat-msg-box")[0].scrollHeight}, 1000);
            var reply_request = $.ajax({
                                type:'POST',
                                url:'api/',
                                data:{
                                umsg:msg,
                                uid:gId,
                                uname:gName,
                                uemail:gEmail,
                                uimage:gImage,
                                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                                },
            });
            reply_request.done(function(data){
                for (var i = 0; i < data['resultsno']; i++) {
                    var item = data['results'][i];
                    if (item['type'] == 'text') {
                        $("<div class = 'msg_ai animated slideInLeft'>" + item['content'] + "</div>").insertBefore(".reference");
                    }
                    else if (item['type'] == 'image') {
                        $("<div class = 'msg_ai animated slideInLeft'><img class='img_ai' src='" + item['content'] + "' alt = 'image'></div>").insertBefore(".reference");
                        getImageSize($('.img_ai').last(), function(width, height){
                            $("#chat-msg-box").stop();
                            $("#chat-msg-box").animate({scrollTop:$("#chat-msg-box")[0].scrollHeight + height}, 1000);
                        });
                    }
                    $("#chat-msg-box").stop();
                    $("#chat-msg-box").animate({scrollTop:$("#chat-msg-box")[0].scrollHeight}, 1000);
                };
            });
            reply_request.fail(function( jqXHR, textStatus ) {
                console.log( "Request failed: " + textStatus );
            });
        }
        else {
            $("#chat-send-button").animateCss('tada');
        }
    });
});
