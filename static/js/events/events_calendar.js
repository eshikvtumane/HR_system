function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}



function stringToMomentDate(str){

    d = parseInt(str.substr(0,2));
    m = parseInt(str.substr(3,5));
    y = parseInt(str.substr(6,10));
    h = parseInt(str.substr(11,13));
    min = parseInt(str.substr(14,15));
    return moment({years:y,months:m-1,days:d,hours:h,minuntes:min});
}


//сохранение событие после изменения(посредством resize или drop)
function changeEvent(event, delta, revertFunction){
    updateEvent(event.id,event.start.format(),event.end.format());
    $('#email_modal').modal('show');


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
                });

        $('#email_modal').modal('show');
        var event = $('#scheduler').fullCalendar('clientEvents',parseInt(event_id));
        $('#email_modal').modal('show');
        console.log(event);

    },
    error: function() {

        $.notify("Произошла ошибка! Попробуйте обновить событие ещё раз",'error',{
                    position : 'top center'
                })
    }
  });


}


function addEvent(event_type,event_start,event_end,app_vacancy_id)
{

    $.ajax({
        url: "/events/add_event",
        type: "POST",
        dataType: "json",
        data:{
            "event_type" : event_type,
            "start" : event_start,
            "end" : event_end,
            "app_vacancy_id" : app_vacancy_id
        },


        success:function(data){
            $.notify("Действие успешно добавлено!",'success',{
                    position : 'top center'
                });
            $('#scheduler').fullCalendar('removeEvents',event_type);
            $('#scheduler').fullCalendar('refetchEvents');

        },

        error:function(data){
             $.notify("Произошла ошибка во время добавления действия!",'success',{
                    position : 'top center'
                })
    }


    } )



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
            $.notify("Действие успешно удалено",'success',{
                    position : 'top center'
                })


        },

        error:function(){

              $.notify("Произошла ошибка! Попробуйте удалить действие ещё раз",'error',{
                    position : 'top center'
                })
        }

    })
}


//открытие диалоговой формы редактирования события
function editEventData(calEvent, jsEvent, view){
    $('#candidate_info').hide();
    $("#event_id").val(calEvent.id);
    $("#title").val(calEvent.title);
    $("#start").val(calEvent.start.format('DD/MM/YYYY HH:mm'));
    $("#end").val(calEvent.end.format('DD/MM/YYYY HH:mm'));
    $('#profile_link').attr('href',calEvent.profile_link);
    $('#candidate_name').html(calEvent.name);
    var $phones =  $('#candidate_phones ul');
    //очищаем список от телефонов, оставшихся с предыдущих вызовов моадльного окна
    $phones.html('');
    calEvent.phones.forEach(function(phone){

        $('<li>'+phone+'</li>').appendTo($phones);

      });


    dialog.dialog( "open" );

}




//при загрузке страницы...
$(function(){


  //Инициализируем диалоговое окно с редактированием события
    dialog = $( "#edit_event" ).dialog({
    autoOpen: false,
    height: 400,
    width: 400,
    modal: true



});
    //инициализируем jqueryui datepicker плагин на форме редактирования события
    $("#start,#end").datetimepicker({ dateFormat: 'dd-mm-yy' });


    form = dialog.find( "form" ).on( "submit", function( event ) {
      event.preventDefault();
    });



   //активируем fullCalendar плагин
    $('#scheduler').fullCalendar({
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
                element.attr(
                {
                    'profile_link':event.profile_link,
                    'name': event.name,
                    'phones':event.phones
                })
        },
        eventResize: changeEvent,
        eventDrop: changeEvent,
        eventClick: editEventData,
        dayClick: function(date,jsEvent,view){
            $('#scheduler').fullCalendar('changeView', 'agendaDay');
            $('#scheduler').fullCalendar('gotoDate', date.format());

        },

        drop: function(date){

            },

        eventReceive:function(event){

                var event_type = event.id;
                var app_vacancy_id = $('#app_vacancy_id').val();
                var start = event.start.format();
                var end = event.end.format();
                addEvent(event_type, start, end, app_vacancy_id);

        }


    });

//показать информацию по кандидату
$('#show_candidate_info').click(function(){
    $('#candidate_info').toggle();
});

//сохранение события при его изменение через диалоговоую форму
$('#save_event').button().on('click',function(){
    var event_id = $("#event_id").val();
    var new_start_time = stringToMomentDate($("#start").val());
    var new_end_time = stringToMomentDate($('#end').val());
    updateEvent(event_id,new_start_time.format(),new_end_time.format());
});

//удаление события
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
				id: $(this).attr('id'),
				stick: true, // maintain when user navigates (see docs on the renderEvent method)
				start: "00:00",
				duration: "03:00"

			});

			// make the event draggable using jQuery UI
			$(this).draggable({
				zIndex: 999,
				revert: true,      // will cause the event to go back to its
				revertDuration: 0  //  original position after the drag
			});

		});


    //сохраняем id вакансии по которой перешли в календарь в скрытом поле
    $('<input>').attr({
         id:'app_vacancy_id',
         type:'hidden',
         value: $.cookie('app_vacancy_id')


    }).appendTo('#external-events');


    //удаляем куку с id вакансии, чтобы исключить возможность назначения действия без перехода
    //со страницы кандидата
    $.cookie('app_vacancy_id',"nothing",{ path: '/',expires:-10000 });


});