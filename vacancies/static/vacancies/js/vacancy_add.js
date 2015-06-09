window.onload = function(){
    //валидация формы

    $.validate({


        form:'#frm_add_vacancy',
        onError : function() {

    },
        onSuccess:function(){

        addVacancy();
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


    //Добавление вакансии
    function addVacancy () {
        var datastring = $('#frm_add_vacancy').serialize();
        $.ajax({
            type: 'Post',
            url: '/vacancies/add/',
            dataType: 'json',
            data: datastring,
            success: function (data) {
               if (data['vacancy_id']){
               var vacancy_id = data["vacancy_id"];
               window.location.href = '/vacancies/' + vacancy_id;
                }

                else {
                        $('#error_box').html(data['errors']);
                    }


            },

            error: function(xhr,errmsg,err) {
                   $.notify("Произошла ошибка при добавлении вакансии!Попробуйте ещё раз!",'error',{
                    position : 'top center'
                });
                    console.log(xhr.status + '' + xhr.responseText);
            }
        });

    }



    //Выборка руководителей отделов
    $('#department').change(function(){
        department = $('#department').val();
        $.ajax({
            type: 'GET',
            url: '/vacancies/get_heads/',
            dataType: 'json',
            data: {'department':department},
            contentType: 'application/json',
            success: function (data) {

               $select =  $('<select/>',{
                   'id': 'heads',
                   'name': 'head',
                   'class': 'form-control'
                });
                $.each(data,function(){
                    $('<option/>',{
                        'value': this['id'],
                        'text': this['name']

                    }).appendTo($select);

                });
                $heads_div = $('#heads_div');
                $heads_div.empty();
                $("<label for='heads'>Руководитель</label>").appendTo($heads_div);
                $select.appendTo(heads_div)
            },
            error: function(xhr,errmsg,err) {
                  $.notify("Произошла ошибка на сервере!Попробуйте ещё раз!",'error',{
                    position : 'top center'
                });
                    console.log(xhr.status + '' + xhr.responseText)
            }
        });
        return false;
    });



   };
