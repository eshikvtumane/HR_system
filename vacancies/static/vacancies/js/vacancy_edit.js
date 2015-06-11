window.onload = function(){
//валидация формы


    $.validate({


        form:'#frm_update_vacancy',
        onError : function() {

    },
        onSuccess:function(){

        updateVacancy();
        return false

        }

    });


// инициализация datepicker
    $('#end_date').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y'
    });


    $('#benefits').selectize({
        maxItems: null
    });


    //Обновление вакансии
    function updateVacancy () {
        var datastring = $('#frm_update_vacancy').serialize();
        var $vacancy_id = $("#vacancy_id").val();
        $.ajax({
            type: 'Post',
            url: '/vacancies/'+ $vacancy_id + '/' + 'edit/',
            dataType: 'json',
            data: datastring,
            success: function (data) {
                if(!data['errors']){
                $.notify("Данные вакансии успешно обновлены",'success',{
                    position : 'top center'
                })
                 }

                else{
                     $.notify('Проверьте правильность заполненных полей!','error',{
                    position : 'top center'
                })
                    $('#error_box').html(data['errors'])

                }

            },
            error: function(xhr,errmsg,err) {
               $.notify("Произошла ошибка при обновлении данных!Попробуйте ещё раз!",'error',{
                    position : 'top center'
                });

                console.log(xhr.status + '' + xhr.responseText)


            }
        });

    }





   };
