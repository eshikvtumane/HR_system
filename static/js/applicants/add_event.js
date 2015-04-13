$(document).ready(function(){

$('.assign_event').click(function(e){
    var $div_modal_footer =  $("#event_modal").find(".modal-footer");
    $div_modal_footer.empty();
    //получаем id вакансии из скрытого элемента input
    var app_vacancy_id =  $(this).parents('.btn-group').find('.vacancy-id').val()
    var $save_event_btn =  $("<button>",{
        'id':'save_event',
        'class': 'btn btn-default',
        'text': 'Назначить',

    });
    $save_event_btn.val(app_vacancy_id.toString());
    $div_modal_footer.append($save_event_btn);


$("#save_event").click(function(){
   var app_vacancy_id = $(this).val()
   var start = $('#id_start').val();
   var end = $('#id_end').val();
   var event_id = $('#id_event').val();
   $.ajax({
    url: "/events/add_event",
    type: "POST",
    data: {
      'app_vacancy_id': app_vacancy_id,
      'start': start,
      'end': end,
      'event_id': event_id

    },
    success: function(data) {
      //if (!data)
      //{
      //  revertFunc();
      //  return;
        $('#event_modal').modal('hide');
        $.notify("Действие успешно добавлено!",'success',{
                    position : 'top center'
                })
        $('#email_modal').modal('show');

      //calendar.fullCalendar('updateEvent', event);
    },
    error: function() {
      alert("error")
    }

    })

})



})


})

