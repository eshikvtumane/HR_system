$(document).ready(function(){
    var id = document.getElementById('id').value;
    var url = '/applicants/view/' + id + '/';

    // инициализация datepicker
    $('#birthday_change').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y',
        mask: true
    });



    // удалить фото
    $('#delete_photo').click(function(){
        var src="/media/default.gif"

        $.ajax({
            type: 'GET',
            url: '/applicants/delete_photo/',
            data:{
                'applicant_id': $('#id').val()
            },
            dataType: 'json',
            success: function(data){
                var code = data[0];
                if(code == '200'){
                    alert('Фото успешно удалено!');
                    $('#imagePreview').attr('src', src);
                }
                else{
                    alert('Произошла ошибка при удалении фото');
                    console.log(data);
                }

            },
            error: function(data){
                alert('Произошла ошибка при удалении фото ()');
                console.log(data);
            }
        });
    });

    // удалить номер телефона
    $('.phone-delete').click(function(){
        var $obj = $(this);
        $.ajax({
            type: 'GET',
            url: '/applicants/delete_phone/',
            data:{
                'phone_id': $obj.attr('id')
            },
            dataType: 'json',
            success: function(data){
                var code = data[0];
                if(code == '200'){
                    alert('Номер телефона успешно удален');
                    $obj.parent().remove();
                }
                else{
                    alert('Произошла ошибка при удалении');
                    console.log(data);
                }

            },
            error: function(data){
                alert('Произошла ошибка при удалении');
                console.log(data);
            }
        });
    });

    $('#birthday_change').change(function(){
        var val = $(this).val();
        if(val != '__-__-____'){
            $('#birthday_hidden').val(val);
        }


    });



// validate_applicant_form.js
    validateForm(sendApplicantForm, url, fn);
});



var fn = function(data){
    var div_result = document.getElementById('create_applicant_message');

    if(data[0] == '200'){
        var url = '/applicants/view/' + data[1] + '/';
        window.location.href = url;
        div_result.innerHTML = 'Обновление данных прошло успешно';
    }
    else{
        div_result.innerHTML = 'Произошла ошибка. Пожалуйста, попробуйте повторить сохранение позднее';
        console.log(data);
    }

    document.getElementById('save_loader').innerHTML = '';
}

