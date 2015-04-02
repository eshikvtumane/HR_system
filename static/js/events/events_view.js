$(function(){
    //при выборе вакансии, делаем запрос на сервер и выводим все события назначенные кандидату по выбранной вакансии
    $('#vacancy_slct').on('change',function(){
       var vacancy_id = $(this).val();

       $.ajax({
        type: 'GET',
        url: '/events/get_vacancy_events/',
        dataType:'json',
        data:{
            'app_vacancy_id': vacancy_id
        },


       success:function(data){
            var field_names =  ['event','start','end','author','happened','description'];
            $('#events_table').find('tbody').empty();
            for (i=0;i<data.length;i++){
                var event = data[i];
                var $row =  $('<tr>');
                for(j=0; j < field_names.length; j++)
                {
                    if (field_names[j] == 'happened'){

                        if (event[field_names[j]]){
                            $("<td>",{

                            }).appendTo($row).append("<input type='checkbox' checked='checked' disabled='disabled'>");



                        }else{

                             $("<td>",{

                            }).appendTo($row).append($('<input>',{

                                type:'checkbox',
                                class : 'is_happened_chk',
                                value: event['id']

                            }));


                        }

                    }
                    else{
                    $('<td>',{
                       text:event[field_names[j]]
                    }).appendTo($row);
                        }

                }


              $('#events_table').find('tbody').append($row);
            };


              $('.is_happened_chk').change(function(){
                $('#event_description_box').dialog('open');


                $('#save_event_btn').val($(this).val());

                 });


       },

       error:function(){
              $('#events_table').find('tbody').empty();
              $('#errors_box').html("ERROR OCCURED!!");
       }


      })

      })

    //активириуем диалоговое окно для добавления описания к событию
    $('#event_description_box').dialog({

            autoOpen:false,
            modal: true

            });

    //сохраняем изменённое состояние события а также его описание, введенное в диалоговом окне в базе данных
    $('#save_event_btn').click(function(){
        var event_id = $(this).val();
        var event_description = $("#event_description_txt").val();
        $.ajax({
            type:'POST',
            url: '/events/change_event_status',
            dataType:'json',
            data:{'event_description': event_description, 'event_id':event_id},
            success:function(data){
                alert('Описание успешно добавлено')
            },
            error:function(){
                alert('Произошла ошибка');
            }
        })

    })

})