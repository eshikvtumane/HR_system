window.onload = function(){


// инициализация datepicker
    $('#end_date').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y'
    });

    $('#btn_save_vacancy').click(function () {
        var datastring = $('#frm_add_vacancy').serialize();
        console.log(datastring)
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




   }
