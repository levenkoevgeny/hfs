$("#education_data_add").click(function() {

    let form_data = $("form").serializeArray();

    $.ajax({
        url: "/profiles/education/add/",
        method: "POST",
        dataType: 'json',
        data: form_data,
        timeout : 100000,
        success: function (data) {
            console.log(data);
            if (data['error']) {
                alert(data['error']);
            } else {
                window.opener.location.href = window.opener.location.href;
                window.close();
            }
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });
});

// function education_delete(){
//     let education_id = $(this).attr('value');
//     alert(education_id);
// }

$(".education_delete_button").click(function() {
    let education_id = $(this).attr('value');

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
        url: "/profiles/education/delete/" + education_id + "/",
        method: "POST",
        timeout : 100000,
        success: function (data) {
            window.location.href = window.location.href;
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });
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


