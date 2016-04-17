
function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}
$.fn.imageLoad = function(fn) {
    this.load(fn);
    this.each(function() {
        if (this.complete && this.naturalWidth !== 0) {
            $(this).trigger('load');
        }
    });
}

$(document).ready(function() {
    var idu;
    $('#chat-message-text').click(function() {
        document.getElementById("user-profile").src = "../static/ai/img/profile.png";
        gapi.client.load('plus', 'v1', function() {
            var request = gapi.client.plus.people.get({
                'userId': 'me'
            });
            request.execute(function(resp) {
                console.log('Retrieved profile for:' + resp.displayName + ' ' + resp.image.url);
                idu = resp;
                if (resp.image.url != 'undefined') {
                    document.getElementById("user-profile").src = resp.image.url;
                }
            });
        });
    });
    $('#signinmodal').on('hidden.bs.modal', function() {
        document.getElementById("user-profile").src = "../static/ai/img/profile.png";
        gapi.client.load('plus', 'v1', function() {
            var request = gapi.client.plus.people.get({
                'userId': 'me'
            });
            request.execute(function(resp) {
                console.log('Retrieved profile for:' + resp.displayName + ' ' + resp.image.url);
                if (resp.image.url != 'undefined') {
                    document.getElementById("user-profile").src = resp.image.url;
                }
            });
        });
    })
    $("#signout").click(
        function logout() {
            gapi.auth.signOut();
            //location.reload();
            gapi.client.load('plus', 'v1', function() {
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
    $("#chat-message-text").keyup(function(event) {
        if (event.keyCode == 13) {
            $("#chat-send-button").click();
        }
    });
    $("#chat-send-button").click(function() {
        var msg = $("#chat-message-text").val();
        if (!isEmptyOrSpaces(msg)) {

            gapi.client.load('plus', 'v1', function() {
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
            $.getJSON('/api/msg=' + urlmsg + '&id=' + idu, function(data, jqXHR) {
                $("#chat-message-text").val("")
                $("<div class = 'msg_user'>" + msg + "</div>").insertBefore(".reference");
                for (var i = 0; i < data['resultsno']; i++) {
                    var item = data['results'][i];
                    if (item['type'] == 'text') {
                        $("<div class = 'msg_ai'>" + item['content'] + "</div>").insertBefore(".reference");
                    } 
                    else if (item['type'] == 'image') {
                        $("<div class = 'msg_ai'><img class='img_ai' src='" + item['content'] + "' alt = 'image'></div>").insertBefore(".reference");
                        //Used so that the scroll is correct once the image is fully loaded
                        $('img.img_ai').imageLoad(function() {
                            $("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
                        });
                    }
                    $("#chat-msg-box").scrollTop($("#chat-msg-box")[0].scrollHeight);
                };
            });
        }
    });
});