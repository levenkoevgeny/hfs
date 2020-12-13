$( document ).ready(function() {
     const chatSocket = new WebSocket(
         'ws://'
         + window.location.host
         + '/ws/message_listener/'
     );

     chatSocket.onmessage = function(e) {
          console.log(e.data);

          // $('#id_toast-body').html(data['last_name'] + ' откликнулся на вакансию ' + data['vacancy_name']);
          // console.log(data['img_url']);
          // $('#profile_img').attr("src", data['img_url']);
          // let td_count = $( '[data-vacancyid=' + data['vacancy_id'] + ']');
          // td_count.html(data['count']);
          // $('.toast').toast('show');
     };

     chatSocket.onclose = function(e) {
          console.error('Chat socket closed unexpectedly', e);
     };
});

