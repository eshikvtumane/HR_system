window.onload = function(){


// инициализация datepicker
    $('#end_date').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y'
    });
    //Сохранение вакансии
    $('#save_vacancy').click(function () {
        var datastring = $('#frm_add_vacancy').serialize();
        console.log(datastring);
        $.ajax({
            type: 'Post',
            url: '/vacancies/add/',
            dataType: 'json',
            data: datastring,
            success: function (data) {
               var vacancy_id = data[0]["vacancy_id"];
               window.location.href = '/vacancies/' + vacancy_id;
            },
            error: function(data) {
                    console.log("ERROR")
            }
        });
        return false;
    });


    //Выборка руководителей отделов
    $('#department').change(function(){
        department = $('#department').val();
        console.log("Get_heads ajax request");
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
            error: function(data) {
               console.log("ERROR, retrieving heads")
            }
        });
        return false;
    });


     //Обновление вакансии
     $('#update_vacancy').click(function () {
        var datastring = $('#frm_update_vacancy').serialize();
        var $vacancy_id = $("#vacancy_id").val();
        console.log(datastring);
        $.ajax({
            type: 'Post',
            url: '/vacancies/'+ $vacancy_id + '/',
            dataType: 'json',
            data: datastring,
            success: function (data) {

               //window.location.href = '/vacancies/' + vacancy_id;
            },
            error: function(data) {
               alert("Произошла ошибка!");
               console.log("ERROR")
            }
        });
        return false;
    });


   };
