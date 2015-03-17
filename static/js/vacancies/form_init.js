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
            data: datastring,
            success: function (data) {
               alert("Вакансия сохранена!");
            },
            error: function(data) {
               alert("Произошла ошибка!");
            }
        });
        return false;
    });

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
                   'name': 'heads',
                   'class': 'form-control'
                });
                $.each(data,function(){
                    $('<option/>',{
                        'value': this['id'],
                        'text': this['name']

                    }).appendTo($select);

                });
                $("<label for='heads' id = 'lbl_heads' >Руководитель</label>").insertAfter('#department');
                $select.insertAfter('#lbl_heads')
            },
            error: function(data) {
               alert("Произошла ошибка!");
            }
        });
        return false;
    });


   }
