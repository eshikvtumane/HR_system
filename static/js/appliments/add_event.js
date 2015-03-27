$(document).ready(function(){

$("#add_event").on('click',function(){

   var applicant_id =  $('#id').val();
   var vacancy_id = $(this).val();
   var start = $('#id_start').val();
   var end = $('#id_end');
   var event_id = $('#id_event')

   $.ajax({
    url: "/view/applicants/"+applicant_id+"/add_event",
    type: "POST",
    dataType: "json",
    data: {
      'applicant_id': applicant_id,
      'vacancy_id': vacancy_id,
      'start': start,
      'end': end,
      'event': event_id

    },
    success: function(data, textStatus) {
      //if (!data)
      //{
      //  revertFunc();
      //  return;
      alert("yooooo");
      //calendar.fullCalendar('updateEvent', event);
    },
    error: function() {
      alert("error")
    }

    })

})


})

