window.onload = function(){
//валидация формы


    $.validate({
        decimalSeparator : ',',


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
               $.notify("Произошла ошибка при обновлении данных!Попробуйте ещё раз!",'error',{
                    position : 'top center'
                })
            }
        });

    }





   };
