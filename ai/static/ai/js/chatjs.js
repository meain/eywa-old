// Global variables for user data
var gId = '';
var gName = '';
var gImage = '';
var gEmail = '';

function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}

function onSignIn(googleUser) {
    // Handle signing the user in using google login
    var profile = googleUser.getBasicProfile();
    gId = profile.getId();
    gName = profile.getName();
    gImage = profile.getImageUrl();
    gEmail = profile.getEmail();
    showSignInOrImg();
}

function signOut() {
    // Sign the user out of google auth
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        gId = '';
        gName = '';
        gImage = '';
        gEmail = '';
        showSignInOrImg();
    });
}

function checkIfSignedIn() {
    // Just check if the user is singned in by checking if user data is available
    if (gId != '') {
        return true;
    } else {
        return false;
    }
}

function showSignInOrImg() {
    // Handles displaying the user data on top in respnse to sign in
    if (checkIfSignedIn()) {
        // If user is signed in display the profile picture and name and hide the sign in button
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
        // Remove suer details and show the google sign in button
        $(".gsignin")[0].style.display = "inline";
        $("#user-name")[0].style.display = "none";
        $("#user-profile")[0].style.display = "none";
        $("#user-name")[0].innerHTML = "";
        $("#user-profile")[0].src = "../static/ai/images/profile.png"
        $("#som-img")[0].src = "../static/ai/images/profile.png"
    }
}

function getImageSize(img, callback) {
    // Function used to get the size of the image before the image is actually fully loaded
    // so that we can correct the scroll even befor the image is actually fully loaded
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

$.fn.extend({
    // Function that is used to do all the animations in animate.css as and when needed
    animateCss: function(animationName) {
        var animationEnd = 'webkitAnimationEnd onanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).removeClass('animated ' + animationName);
        });
    }
});

$('#chat-msg-box').scroll(function(e) {
    // Bodge to work arround the chat-msg-box from scrolling even after it has reached the end
    if ($('#chat-msg-box').scrollTop() + $('#chat-msg-box').innerHeight() >= $('#chat-msg-box')[0].scrollHeight) {
        $('#chat-msg-box').finish();
    }
});

function formatRequest(msg){
    // Get user data in json string format
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
socket.onopen = function() {}

$(document).ready(function() {
    // Focus the chat input box
    $("#chat-message-text").focus();

    // Show sign in options or user data
    showSignInOrImg();

    $("#user-profile").click(function(e) {
        // On click on users profile image show a dialog with signout options
        e.stopPropagation();
        displayPopup('#user-profile', '#signinpopup', 'left', 'below', true, 'white', 7);
    });

    $("#som-signout").click(function() {
        // On clicking on signout button in the popup sign the user out of the service
        signOut();
        removePopup("#signinpopup");
    });

    $("#chat-message-text").keyup(function(event) {
        // Make enter key work like send button
        if (event.keyCode == 13) {
            $("#chat-send-button").click();
        }
    });

    $("#chat-send-button").click(function() {
        /*
        * Function to be excecuted on the send button click
        */
        // Get user input
        var msg = $("#chat-message-text").val();

        if (!isEmptyOrSpaces(msg)) { // Only of the user input is not spaces
            $("#chat-send-button").animateCss('flash'); // Send animation
            $("#chat-message-text").val("") // Remove text
            // Add the user message
            $("<div class = 'msg_user animated fadeIn'>" + msg + "</div>").insertBefore(".reference");

            // Scroll the chat window
            $("#chat-msg-box").stop();
            $("#chat-msg-box").animate({
                scrollTop: $("#chat-msg-box")[0].scrollHeight
            }, 9000, 'easeOutExpo');

            // Send the user input through WebSocket connection
            socket.send(formatRequest(msg));
            socket.onmessage = function(e) {
                // On reciving the result back from the server
                data = JSON.parse(e.data);
                for (var i = 0; i < data['resultsno']; i++) { // Result is an array of dicts
                    var item = data['results'][i];
                    if (item['type'] == 'text') { // text result
                        $("<div class = 'msg_ai animated fadeIn'>" + item['content'] + "</div>").insertBefore(".reference");
                    } else if (item['type'] == 'image') { // image result
                        $("<div class = 'msg_ai animated fadeIn'><img class='img_ai' src='" + item['content'] + "' alt = 'image'></div>").insertBefore(".reference");

                        // Set image click action to popup
                        $('.img_ai').click(function(e){
                            e.stopPropagation();
                            var aiMsgImage = e.target.src;
                            $("#fullscreenimage").attr("src", aiMsgImage);
                            displayFullScreenPopup("#popupboximagecontent");
                        });

                        // Initiate smart scroll in case of image by getting the image height ahed of time
                        getImageSize($('.img_ai').last(), function(width, height) {
                            $("#chat-msg-box").stop();
                            $("#chat-msg-box").animate({
                                scrollTop: $("#chat-msg-box")[0].scrollHeight + height
                            }, 9000, 'easeOutExpo');
                        });
                    }

                    // Scroll the chat window
                    $("#chat-msg-box").stop();
                    $("#chat-msg-box").animate({
                        scrollTop: $("#chat-msg-box")[0].scrollHeight
                    }, 9000, 'easeOutExpo');
                };
            }

        }
        else {
            // In case the user input is null, jsut show an animations to show invalid input
            $("#chat-send-button").animateCss('tada');
        }
    });
});
