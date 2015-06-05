$(function(){

    var $comment_block = "";
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
            //создаём массив для вывода полей из json-response-object в определённом порядке
            var field_names =  ['event','start','end','author','description'];
            $('#events_table').find('tbody').empty();
            for (i=0;i<data.length;i++){
                var event = data[i];
                var $row =  $('<tr>');
                for(j=0; j < field_names.length; j++)
                {

                       $('<td>',{
                           text:event[field_names[j]]
                        }).appendTo($row);


                }

                var $btn_cmnt =  $("<button class='btn_comment'>",{

                }).html("<i class='fa fa-pencil'></i> Комментировать").val(vacancy_id);

                $('<td>',{
                           text:event[field_names[j]]
                        }).append($btn_cmnt).appendTo($row);


              $('#events_table').find('tbody').append($row);
            };

              $('.btn_comment').click(function(){
                //создаём указатель на чекбокс, чтобы в дальнейшем обратиться к нему
                var $btn = $(this);
                $comment_block = $btn.parent().prev();
                var comment = $comment_block.html();
                $('#event_description_txt').html(comment);
                $('#event_description_box').dialog('open');

                //если пользователь решил не изменять состояние события и закрыл диалоговое окно

                $('#save_event_btn').val($btn.val());

                 });


       },

       error:function(){
              $('#events_table').find('tbody').empty();

       }


      })

      });

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
            url: '/events/add_event_comment',
            dataType:'json',
            data:{'event_description': event_description, 'event_id':event_id},
            success:function(data){
                $comment_block.html(event_description);
                $('#event_description_box').dialog('close');
                 $.notify("Комментарий успешно добавлен!",'success',{
                    position : 'top center'
                })
            },
            error:function(){
                alert('Произошла ошибка');
            }
        })

    })

})