$( document ).ready(function() {

    $('.vacancy_respond').removeAttr("disabled");

    $('.vacancy_respond').on( "click", function() {
        let vacancy_id = $(this).data('vacancyid');
        let response_sign = Number.parseInt($(this).val());
        get_response(vacancy_id, response_sign);
    });

});

function get_response(vacancy_id, response_sign){

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

    let response_data = {}
    response_data["vacancy_id"] = vacancy_id;
    response_data["response_sign"] = response_sign;
    $.ajax({
        url: "/institution/vacancy/getresponse",
        type: "POST",
        dataType: 'json',
        data: response_data,
        timeout : 100000,
        success: function (data) {
            change_response_button(data);
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });

}


function change_response_button(data){
    let sign = Number.parseInt(data['sign']);
    let vacancy_id_val = String(data['vacancy_id']);
    let response_button = $( '[data-vacancyid=' + vacancy_id_val + ']');
    if (sign === 1) {
        response_button.removeClass('btn-secondary').addClass('btn-success');
        response_button.html("<i class=\"fas fa-bell\"></i> Вы откликнулись на эту вакансию");
    }
    if (sign === -1) {
        response_button.removeClass('btn-success').addClass('btn-secondary');
        response_button.html("<i class=\"fas fa-bell\"></i> Откликнуться на вакансию");
    }
    response_button.val(sign);
}
