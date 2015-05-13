//конвертация даты в виде текста в объект Moment
function stringToMomentDate(str){

    d = parseInt(str.substr(0,2));
    m = parseInt(str.substr(3,5));
    y = parseInt(str.substr(6,10));
    h = parseInt(str.substr(11,13));
    min = parseInt(str.substr(14,15));
    return moment({years:y,months:m-1,days:d,hours:h,minuntes:min});
}


//изменение события (посредством resize или drop)
function changeEvent(event, delta, revertFunction){
    updateEvent(event.id,event.start.format(),event.end.format());



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

        //если форма с редактированием события была открыта,то закрываем её
        if ($("#edit_event").attr('display') !== 'none'){
                dialog.dialog('close');
        }

        $.notify("Событие успешно обновлено! Возможно, вам стоит отправить кандидату оповещение об изменённом событии.",
        'success',{
                    position : 'top center'
                });

        //перезагружаем события
         $('#scheduler').fullCalendar('refetchEvents');


    },
    error: function() {

        $.notify("Произошла ошибка! Попробуйте обновить событие ещё раз",'error',{
                    position : 'top center'
                })
    }
  });


}

//добавление нового события через календарь
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

    $("#event_id").val(calEvent.id);
    $("#title").val(calEvent.title);
    $("#start").val(calEvent.start.format('DD/MM/YYYY HH:mm'));
    $("#end").val(calEvent.end.format('DD/MM/YYYY HH:mm'));
    $('#profile_link').attr('href',calEvent.profile_link);
    $('#candidate_name').html(calEvent.name);
    $('#event_author').html(calEvent.author);
    $('#candidate_email').html(calEvent.email);
    var $phones =  $('#candidate_phones ul');
    //очищаем список от телефонов, оставшихся с предыдущих вызовов моадльного окна
    $phones.html('');
    calEvent.phones.forEach(function(phone){

        $('<li>'+phone+'</li>').appendTo($phones);

      });


    dialog.dialog( "open" );

}



//список праздничных дней
var holidays = new Array();
//при загрузке страницы...
$(function(){
      //Инициализируем диалоговое окно с редактированием события
        dialog = $( "#edit_event" ).dialog({
        autoOpen: false,
        height: 350,
        width: 600,
        modal: true

    });

    // Получаем список праздничных и предпразничных дней
    $.ajax({
        url: 'http://basicdata.ru/api/json/calend/',
        crossDomain: true,
        dataType: 'jsonp',
        jsonp: 'jsonp_callback',
        success: function(data){
            holidays = data;
        },
        error: function(){
            holidays = [];
            console.log('Error get holidays');
        }
    });

      var event_remove_dialog =$( "#event_remove_confirm" ).dialog({
      autoOpen: false,
      resizable: false,
      height:200,
      modal: true,
      buttons: {
        "Удалить действие": function() {
          $( this ).dialog( "close" );
        },
        "Отмена": function() {
          $( this ).dialog( "close" );
        }
      }
    });


    //инициализируем jqueryui datepicker плагин на форме редактирования события
    $("#start,#end").datetimepicker($.extend($.datepicker.regional['ru'], {
        dateFormat: 'dd-mm-yy',
        stepMinute: 15
    }));


    form = dialog.find( "form" ).on( "submit", function( e ) {
      e.preventDefault();
    });

/* инициализируем внешние события
		-----------------------------------------------------------------*/


		$('#external-events .fc-event').each(function() {
			// добавляем данные к внешним событиям
			$(this).data('event', {
				title: $.trim($(this).text()), //используем текст элемента в качестве заголовкка события
				id: $(this).attr('id'),
				stick: true,
				start: "09:00",
				duration: "01:00"
			});

			// делаем событие draggable
			$(this).draggable({
				zIndex: 999,
				revert: true,
				revertDuration: 0
			});

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
        slotDuration: moment.duration('00:15:00'),
        minTime: moment.duration('09:00:00'),
        maxTime: moment.duration('18:00:00'),
        timezone:'Asia/Vladivostok',
        events:'/events/get_events/',
        hiddenDays: [0, 6],
        eventRender:function(event,element,view){
                //добавляем кастомные атрибуты к загружаемым в календарь событиям
                element.attr(
                {
                    'profile_link':event.profile_link,
                    'name': event.name,
                    'phones':event.phones,
                    'email':event.email,
                    'author':event.author
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

        //обработка добавления внешнего события
        eventReceive:function(event){

                var event_type = event.id;
                var app_vacancy_id = $('#app_vacancy_id').val();
                var start = event.start.format();
                var end = event.end.format();
                addEvent(event_type, start, end, app_vacancy_id);

        },
        dayRender: function(date, cell, view){
            // изменение стиля ячейки, отображающий праздничный день
            var buf_date = String(date.date()) + '-' + String(date.month()) + '-' + String(date.year());
            var date_now = new Date()
            var date_now = date_now.getDate() + '-' + date_now.getMonth() + '-' + date_now.getFullYear()

            // Если текущий день совпадает с обрабатываемым днём, то пропускаем операцию изменения стиля
            if(buf_date !== date_now){
                try{
                    var day_status = holidays[String(date.year())][String(date.year(date.month()+1))][String(date.date())]['isWorking'];
                }
                catch(err){
                    var day_status = 0
                }

                if(day_status == '2'){
                    // праздничный день
                    cell.css('background-color', '#ffdada');
                }
                else if(day_status == '3'){
                    // Предпраздничный день
                    cell.css('background-color', '#ddfffb');
                }
                else{

                }
            }
        }

    });



//открытие окна с отправлением оповещения
$('#open_notification').on('click',function(){
    //закрываем окно с редактированием события(иначе при открытии формы с отправлением оповещения и при последующем
    //клике по инпутам получим ошибку с рекурсией)
    dialog.dialog('close');
    var event_id = $("#event_id").val();
    var event = $('#scheduler').fullCalendar('clientEvents',parseInt(event_id))[0];
    $('#emailto').val(event.email);
    $('#subject').val(event.title);
    $('#message').val("Уважаемый " + event.name + "! Вам назначено " + event.title + " на " + event.start.format
    ('DD/MM/YYYY HH:mm'));
    $('#email_modal').modal('show');




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
     event_remove_dialog.dialog( "open" );
    //deleteEvent(event_id);
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