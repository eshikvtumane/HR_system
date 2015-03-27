$(document).ready(function(){

$('#add_event').click(function(){
    var $div_modal_footer =  $("#event_modal").find(".modal-footer");
    $div_modal_footer.empty();
    var vacancy_id = $(this).val();
    var $save_event_btn =  $("<button>",{
        'id':'save_event',
        'class': 'btn btn-default',
        'text': 'Назначить'
    })
    $save_event_btn.val(vacancy_id.toString());
    $div_modal_footer.append($save_event_btn);


$("#save_event").click(function(){
   var applicant_id =  $('#id').val();
   var vacancy_id = $(this).val();
   var start = $('#id_start').val();
   var end = $('#id_end').val();
   var event_id = $('#id_event').val()
   $.ajax({
    url: "/applicants/view/"+applicant_id+"/add_event/",
    type: "POST",
    dataType: "json",
    data: {
      'vacancy_id': vacancy_id,
      'start': start,
      'end': end,
      'event': event_id

    },
    success: function(data) {
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


})

