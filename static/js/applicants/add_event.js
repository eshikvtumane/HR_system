$(document).ready(function(){

$('.assign_event').click(function(e){
   var app_vacancy_id = $(this).parents('.btn-group').find('.app-vacancy-id').val();
   $.cookie('app_vacancy_id',app_vacancy_id,{ path: '/' });
   window.open('/events/events_calendar/','_blank');


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

