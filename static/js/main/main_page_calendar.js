

function saveData(event, delta, revertFunction){
  $.ajax({
    url: "/vacancies/update_event/",
    type: "POST",
    dataType: "json",
    data: {
      'id': event.id,
      'start': event.start.format(),
      'end': event.end.format()
    },
    success: function(data, textStatus) {
      //if (!data)
      //{
      //  revertFunc();
      //  return;
      alert("success");
      //calendar.fullCalendar('updateEvent', event);
    },
    error: function() {
      alert("error")
    }
  });

}


function editEventData(calEvent, jsEvent, view){
    $("#event_id").val(calEvent.id);
    $("#title").val(calEvent.title);
    $("#start").val(calEvent.start.format('DD/MM/YYYY'));
    $("#end").val(calEvent.end.format('DD/MM/YYYY hh:mm'));

  //
  //$('#start').datetimepicker({
  //      lang: 'ru',
  //      timepicker: true,
  //      format: 'd-m-Y'
  //  });

    //


    dialog.dialog( "open" );

}


$(function(){


  //Initializing fullcalendar add_event dialog form
    dialog = $( "#dialog_form" ).dialog({
    autoOpen: false,
    height: 300,
    width: 350,
    modal: true



});

    $("#start,#end").datetimepicker();

    form = dialog.find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
    });



   //активируем fullCalendar плагин
    $('#scheduler').fullCalendar({
        // put your options and callbacks here

        header: {
        left: 'prev,next,today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay'
      },
        lang:'ru',
        weekMode: 'liquid',
        editable: true,
        droppable: true,
        url: '#',
        allDay: false,
        slotMinutes: 5,
        timezone:'Asia/Vladivostok',
        events:'/vacancies/get_events/',
        eventResize: saveData,
        eventDrop: saveData,
        eventClick: editEventData,
        dayClick: function(date,jsEvent,view){
            $('#scheduler').fullCalendar('changeView', 'agendaDay');
            $('#scheduler').fullCalendar('gotoDate', date.format());

        }


    });


$('#save_event').button().on('click',function(){
    var event_id = $("#event_id").val();
    var event = $('#scheduler').fullCalendar('clientEvents',event_id);
    var new_start_time = $("#start").val();
    var new_end_time = $('#end').val();
    console.log(event);
    $.ajax({
    url: "/vacancies/save_event/",
    type: "POST",
    dataType: "json",
    data: {
      'id': event_id,
      'start': new_start_time,
      'end': new_end_time
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
  });
});




		/* initialize the external events
		-----------------------------------------------------------------*/

		$('#external-events .fc-event').each(function() {

			// store data so the calendar knows to render an event upon drop
			$(this).data('event', {
				title: $.trim($(this).text()), // use the element's text as the event title
				stick: true // maintain when user navigates (see docs on the renderEvent method)
			});

			// make the event draggable using jQuery UI
			$(this).draggable({
				zIndex: 999,
				revert: true,      // will cause the event to go back to its
				revertDuration: 0  //  original position after the drag
			});

		});




})