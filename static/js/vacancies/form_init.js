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

    $('#department').change(function(){
        department_par = $('#department').val();
        console.log("Get_heads ajax request")
        $.ajax({
            type: 'POST',
            url: '/vacancies/get_heads/',
            data: {'department':'dsds','name':'dsdffsfsf'},
            contentType: 'application/json',
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
