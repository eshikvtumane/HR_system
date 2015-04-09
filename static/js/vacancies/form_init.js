window.onload = function(){


// инициализация datepicker
    $('#end_date').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y'
    });
    //Добавление вакансии
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
        $.ajax({
            type: 'Post',
            url: '/vacancies/'+ $vacancy_id + '/' + 'edit/',
            dataType: 'json',
            data: datastring,
            success: function (data) {
               /* var errors = data[0]['errors'];
                for (var key in errors){
                    if(errors.hasOwnProperty(key)){
                        $("<span/>",{
                            text:key+":"+errors[key]
                        }).appendTo("#error_list");
                        console.log(key + "- >" + errors[key]);
                    }
                }*/
                $.notify("Данные вакансии успешно обновлены",'success',{
                    position : 'top center'
                })
            },
            error: function(data) {
               alert("Произошла ошибка!");
               console.log("ERROR")
            }
        });
        return false;
    });


   };
