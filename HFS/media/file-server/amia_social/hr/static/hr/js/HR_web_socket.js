const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/hr/'
);

chatSocket.onmessage = function(e) {
     const data = JSON.parse(e.data);
     console.log(data);
     $('#id_toast-body').html(data['last_name'] + ' откликнулся на вакансию ' + data['vacancy_name']);
     console.log(data['img_url']);
     $('#profile_img').attr("src", data['img_url']);
     let td_count = $( '[data-vacancyid=' + data['vacancy_id'] + ']');
     td_count.html(data['count']);
     $('.toast').toast('show');
};

chatSocket.onclose = function(e) {
     console.error('Chat socket closed unexpectedly', e);
};
