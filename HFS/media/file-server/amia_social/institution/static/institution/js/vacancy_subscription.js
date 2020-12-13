$( document ).ready(function() {

    $('#id_vacancy_subscribe').removeAttr("disabled");

    $('#id_vacancy_subscribe').on( "click", function() {
        let institution_id = $('#institution_id').val();
        let subscribe_sign = Number.parseInt($(this).val());
        get_subscribe(institution_id, subscribe_sign);
    });
});


function get_subscribe(institution_id, subscribe_sign){

    var csrftoken = getCookie('csrftoken');

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

    let subscribe_data = {}
    subscribe_data["institution_id"] = institution_id;
    subscribe_data["subscribe_sign"] = subscribe_sign;
    $.ajax({
        url: "/institution/getsubscription",
        type: "POST",
        dataType: 'json',
        data: subscribe_data,
        timeout : 100000,
        success: function (data) {
            console.log(data);
            change_button(data);
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });
}

function change_button(data){
    let sign = Number.parseInt(data['sign']);
    let subscribe_button = $('#id_vacancy_subscribe');
    if (sign === 1) {
        subscribe_button.removeClass('btn-secondary').addClass('btn-success');
        subscribe_button.html("<i class=\"fas fa-bell\"></i> Отписаться от получения информации о новых вакансиях");
    }
    if (sign === -1) {
        subscribe_button.removeClass('btn-success').addClass('btn-secondary');
        subscribe_button.html("<i class=\"fas fa-bell\"></i> Подписаться на получение информации о новых вакансиях");
    }
    subscribe_button.val(sign);
}

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