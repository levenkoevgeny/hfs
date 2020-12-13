$("#id_profile_image").change(function() {

$("#profile_image_form").submit();

    // let form_data = $("form").serializeArray();

    // $.ajax({
    //     url: "/profiles/skill/add/",
    //
    //     data: form_data,
    //     cache: false,
    //     contentType: false,
    //     processData: false,
    //     method: 'POST',
    //     timeout : 100000,
    //     success: function (data) {
    //         console.log(data);
    //         if (data['error']) {
    //             alert(data['error']);
    //         } else {
    //             window.opener.location.href = window.opener.location.href;
    //             window.close();
    //         }
    //     },
    //     error: function (e) {
    //         console.log("ERROR: ", e);
    //     },
    //     done: function (e) {
    //         console.log("DONE");
    //     }
    // });
});