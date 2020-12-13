$("#personal_data_update").click(function() {

    let form_data = $("form").serializeArray();
    let profile_id = $('#profile_id').val();

    $.ajax({
        url: "/profiles/update/personal_data/" + profile_id + "/",
        method: "POST",
        dataType: 'json',
        data: form_data,
        timeout : 100000,
        success: function (data) {
            // window.opener.$('#id_last_name').val(data['last_name']);
            // window.opener.$('#id_first_name').val(data['first_name']);
            // window.opener.$('#id_patronymic').val(data['patronymic']);
            // window.opener.$('#id_email').val(data['email']);
            // window.opener.$('#id_date_of_birth').val(data['date_of_birth']);
            // window.opener.$('#id_about_myself').val(data['about_myself']);
            // window.opener.$('#id_contact_information_phone').val(data['contact_information_phone']);
            // window.opener.$('#id_contact_information_address').val(data['contact_information_address']);
            // window.close();
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });
});


