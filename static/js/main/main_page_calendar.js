
//сохранение событие после изменения(посредством resize или drop)
function changeEvent(event, delta, revertFunction){
      console.dir(event.start);
    updateEvent(event.id,event.start.format(),event.end.format())

}

//отправка изменённых данных события на сервер
function updateEvent(event_id,event_start,event_end){
    $.ajax({
    url: "/events/update_event/",
    type: "POST",
    dataType: "json",
    data: {
      'id': event_id,
      'start': event_start,
      'end': event_end
    },
    success: function(data, textStatus) {
      //if (!data)
      //{
      //  revertFunc();
      //  return;
      //calendar.fullCalendar('updateEvent', event);
        if ($("#edit_event").attr('display') !== 'none'){
                dialog.dialog('close');
        }
        $.notify("Событие успешно обновлено",'success',{
                    position : 'top center'
                })
    },
    error: function() {

        $.notify("Произошла ошибка! Попробуйте обновить событие ещё раз",'error',{
                    position : 'top center'
                })
    }
  });


}


//удаление действия через диалогвоое окно
function deleteEvent(event_id)
{
    $.ajax({

        url:'/events/delete_event/',
        type: 'POST',
        data: {
            'event_id':event_id
        },
        success:function(data){
           if ($("#edit_event").attr('display') !== 'none'){
                dialog.dialog('close');

          }


            $('#scheduler').fullCalendar('removeEvents',event_id);
            $.notify("Событие успешно удалено",'success',{
                    position : 'top center'
                })


        },

        error:function(){

              $.notify("Произошла ошибка! Попробуйте удалить событие ещё раз",'error',{
                    position : 'top center'
                })
        }

    })
}








//открытие диалоговой формы редактирования события
function editEventData(calEvent, jsEvent, view){
    $("#event_id").val(calEvent.id);
    $("#title").val(calEvent.title);
    $("#start").val(calEvent.start.format('DD/MM/YYYY HH:mm'));
    $("#end").val(calEvent.end.format('DD/MM/YYYY HH:mm'));
    $('#profile_link').attr('href',calEvent.profile_link)
    dialog.dialog( "open" );

}



function stringToMomentDate(str){
    console.log(str);
    d = parseInt(str.substr(0,2));
    m = parseInt(str.substr(3,5));
    y = parseInt(str.substr(6,10));
    h = parseInt(str.substr(11,13));
    min = parseInt(str.substr(14,15));
    return moment({years:y,months:m-1,days:d,hours:h,minuntes:min});
}




//при загрузке страницы...
$(function(){


  //Инициализируем диалоговое окно с редактированием события
    dialog = $( "#edit_event" ).dialog({
    autoOpen: false,
    height: 350,
    width: 400,
    modal: true



});
    //инициализируем jqueryui datepicker плагин на форме редактирования события
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
        events:'/events/get_events/',
        eventRender:function(event,element,view){
                element.attr('profile_link',event.profile_link)
        },
        eventResize: changeEvent,
        eventDrop: changeEvent,
        eventClick: editEventData,
        dayClick: function(date,jsEvent,view){
            $('#scheduler').fullCalendar('changeView', 'agendaDay');
            $('#scheduler').fullCalendar('gotoDate', date.format());

        }


    });

//сохранение события при его изменение через диалоговоую форму
$('#save_event').button().on('click',function(){
    var event_id = $("#event_id").val();
    var new_start_time = stringToMomentDate($("#start").val());
    var new_end_time = stringToMomentDate($('#end').val());
    updateEvent(event_id,new_start_time.format(),new_end_time.format());
});

$('#delete_event').button().on('click',function(){
    var event_id = $("#event_id").val();
    deleteEvent(event_id);
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




});