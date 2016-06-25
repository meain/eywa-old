var gId = '';
var gName = '';
var gImage = '';
var gEmail = '';

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    /* console.log('ID: ' + profile.getId()); */
    /* console.log('Name: ' + profile.getName()); */
    /* console.log('Image URL: ' + profile.getImageUrl()); */
    /* console.log('Email: ' + profile.getEmail()); */
    //Save data
    gId = profile.getId();
    gName = profile.getName();
    gImage = profile.getImageUrl();
    gEmail = profile.getEmail();
    showSignInOrImg();
}

function checkIfSignedIn() {
    if (gId != '') {
        return true;
    } else {
        return false;
        console.log("User not signed in");
    }
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        console.log('User signed out.');
        gId = '';
        gName = '';
        gImage = '';
        gEmail = '';
        showSignInOrImg();
    });
}

function showSignInOrImg() {
    if (checkIfSignedIn()) {
        $("#user-profile")[0].style.display = "inline";
        $(".gsignin")[0].style.display = "none";
        $("#user-name")[0].style.display = "inline-block";
        $("#user-name")[0].innerHTML = gName;
        if (gImage.indexOf("http") > -1) {
            $("#user-profile")[0].src = gImage
        }
        // For signout popup
        $("#som-u-name")[0].innerHTML = gName;
        $("#som-u-email")[0].innerHTML = gEmail;
        if (gImage.indexOf("http") > -1) {
            $("#som-img")[0].src = gImage
        }
    } else {
        $(".gsignin")[0].style.display = "inline";
        $("#user-name")[0].style.display = "none";
        $("#user-profile")[0].style.display = "none";
        $("#user-name")[0].innerHTML = "";
        $("#user-profile")[0].src = "../static/ai/images/profile.png"
        $("#som-img")[0].src = "../static/ai/images/profile.png"
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
    animateCss: function(animationName) {
        var animationEnd = 'webkitAnimationEnd onanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).removeClass('animated ' + animationName);
        });
    }
});
$('#chat-msg-box').scroll(function(e) {
    console.log($('#chat-msg-box').scrollTop() + $('#chat-msg-box').innerHeight() >= $('#chat-msg-box')[0].scrollHeight);
    if ($('#chat-msg-box').scrollTop() + $('#chat-msg-box').innerHeight() >= $('#chat-msg-box')[0].scrollHeight) {
        $('#chat-msg-box').finish();
    }
});

// Get user data in json string format
function getUserInfo(msg){
    var user_data = {};
    user_data['msg'] = msg;
    user_data['id'] = gId;
    user_data['name'] = gName;
    user_data['email'] = gEmail;
    user_data['image'] = gImage;
    data = JSON.stringify(user_data);
    return data;
}

// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers
socket = new WebSocket("ws://" + window.location.host + "/ai/");
socket.onopen = function() {
    console.log('Socket open');
}

$(document).ready(function() {
    $("#chat-message-text").focus();
    showSignInOrImg();
    var idu;
    $("#user-profile").click(function(e) {
        e.stopPropagation();
        displayPopup('#user-profile', '#signinpopup', 'left', 'below', true, 'white', 7);
    });
    $("#som-signout").click(function() {
        signOut();
        removePopup("#signinpopup");
    });
    $("#chat-message-text").keyup(function(event) {
        if (event.keyCode == 13) {
            $("#chat-send-button").click();
        }
    });
    $("#chat-send-button").click(function() {
        var msg = $("#chat-message-text").val();
        if (!isEmptyOrSpaces(msg)) {
            $("#chat-send-button").animateCss('flash');
            $("#chat-message-text").val("")
            $("<div class = 'msg_user animated fadeIn'>" + msg + "</div>").insertBefore(".reference");
            $("#chat-msg-box").stop();
            $("#chat-msg-box").animate({
                scrollTop: $("#chat-msg-box")[0].scrollHeight
            }, 9000, 'easeOutExpo');
            socket.send(getUserInfo(msg));
            socket.onmessage = function(e) {
                data = JSON.parse(e.data);
                console.log(data);
                for (var i = 0; i < data['resultsno']; i++) {
                    var item = data['results'][i];
                    if (item['type'] == 'text') {
                        $("<div class = 'msg_ai animated fadeIn'>" + item['content'] + "</div>").insertBefore(".reference");
                    } else if (item['type'] == 'image') {
                        $("<div class = 'msg_ai animated fadeIn'><img class='img_ai' src='" + item['content'] + "' alt = 'image'></div>").insertBefore(".reference");
                        $('.img_ai').click(function(e){
                            e.stopPropagation();
                            var aiMsgImage = e.target.src;
                            $("#fullscreenimage").attr("src", aiMsgImage);
                            displayFullScreenPopup("#popupboximagecontent");
                        });
                        getImageSize($('.img_ai').last(), function(width, height) {
                            $("#chat-msg-box").stop();
                            $("#chat-msg-box").animate({
                                scrollTop: $("#chat-msg-box")[0].scrollHeight + height
                            }, 9000, 'easeOutExpo');
                        });
                    }
                    $("#chat-msg-box").stop();
                    $("#chat-msg-box").animate({
                        scrollTop: $("#chat-msg-box")[0].scrollHeight
                    }, 9000, 'easeOutExpo');
                };
            }
        }
        else {
            $("#chat-send-button").animateCss('tada');
        }
    });
});
