window.onload = function(){
    //валидация формы

    $.validate({
       


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



    //Добавление вакансии
    function addVacancy () {
        var datastring = $('#frm_add_vacancy').serialize();
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
            error: function(data) {
               console.log("ERROR, retrieving heads")
            }
        });
        return false;
    });



   };
