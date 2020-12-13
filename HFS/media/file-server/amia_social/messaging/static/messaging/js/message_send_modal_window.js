$("#id_message_send_model_button").click(function() {

    let data = {};
    data.message = $("#id_message_text").val();
    data.send_to_id = $("#profile_id").val();

    let csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $.ajax({
        url: "/messaging/send_modal_message/",
        method: "POST",
        dataType: 'json',
        data: data,
        timeout : 100000,
        success: function (data) {
            console.log('modal_send', data);
            // if (data['error']) {
            //     alert(data['error']);
            // } else {
            //     window.opener.location.href = window.opener.location.href;
            //     window.close();
            // }
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


});