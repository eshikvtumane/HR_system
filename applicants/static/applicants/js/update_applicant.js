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


    // модель телефонов
    var phone_model = {
        current_phone: {},
        phones: []
    }
    // представление телефонов
    var phone_view = {
        init: function(){
            //Собираем все телефоны кандидата

            $('#number_phones_list').find('.number-phone-box').each(function(index){
                var dict_phone_attr = {}

                dict_phone_attr['id'] = $(this).find('.phone-id').attr('id');
                dict_phone_attr['phone_number'] = $(this).find('.phone-number').text();

                phone_model.phones.push(dict_phone_attr);
            });
        },
        write_phone_in_field: function(phone){
            $('#edit_number_phone').val(phone);
        },
        get_new_phone: function(){
            return $('#edit_number_phone').val();
        },
        change_phone_on_page: function(){
            $('#phone_id_' + phone_model.current_phone['id']).text($('#edit_number_phone').val());
        }
    }

    var phone_octopus = {
        init: function(){
            phone_view.init();
        },
        data: function(){
            console.log(phone_model.phones);
        },
        edit: function(id){
            var len = phone_model.phones.length;
            for(var i=0; i < len; i++){
                if(phone_model.phones[i]['id'] == id){
                    phone_model.current_phone = phone_model.phones[i];
                    break;
                }
            }


            console.log(phone_model.current_phone)
            phone_view.write_phone_in_field(phone_model.current_phone['phone_number']);
        },
        save_change: function(){
            var data = {
                'id': phone_model.current_phone['id'],
                'phone': phone_view.get_new_phone()
            }
            phone_octopus.ajax_send('/applicants/change_phone/', data, 'Номер успешно изменён', 'Произошла ошибка при изменении номера')

            phone_view.change_phone_on_page();
        },
        remove: function(){

        },
        ajax_send: function(url, data, success_msg, error_msg){
            $.ajax({
                type: 'GET',
                url: url,
                data: data,
                dataType: 'json',
                success: function(data){
                    var code = data[0];
                    if(code == '200'){
                        alert(success_msg);
                    }
                    else{
                        alert(error_msg);
                        console.log(data);
                    }

                },
                error: function(data){
                    alert('Произошла ошибка при изменении номера');
                    console.log(data);
                }
            });
        }
    }

    // удалить номер телефона
    $('.phone-delete').click(function(){
        var $obj = $(this);
        var data = {
            'phone_id': $obj.parent().find('.phone-id').attr('id')
        }

        deleteInfo('/applicants/delete_phone/', data, $obj, 'Номер телефона успешно удален');
    });

    // инициализируем работу с телефонами
    phone_octopus.init();
    phone_octopus.data();

    $('.phone-edit').click(function(){
        var $obj = $(this);
        // ищем label с номером телефона
        var phone_id = $obj.parent().find('.phone-id').attr('id');
        phone_octopus.edit(phone_id);
    });

    // сохранение изменённого номера
    $('#change_phone_number').click(function(){
        phone_octopus.save_change();
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


    // удалить образование
    $('.education-delete').click(function(){
        var $obj = $(this);
        var data = {
            'edu_id': $obj.attr('id')
        };
        deleteInfo('/applicants/delete_education/', data, $obj, 'Запись о образовании успешно удалена');
    });

    // удалить портфолио
    $('.portfolio-delete').click(function(){
        var $obj = $(this);
        var data = {
            'portfolio_id': $obj.attr('id')
        };

        deleteInfo('/applicants/delete_portfolio/', data, $obj, 'Портфолио успешно удалено');
    });

    // удалить резюме
    $('.resume-delete').click(function(){
        var $obj = $(this);

        var data = {
            'resume_id': $obj.attr('id')
        };

        deleteInfo('/applicants/delete_resume/', data, $obj, 'Резюме успешно удалено');
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

// удаление информации о кандидате
function deleteInfo(url, data, $obj, success_message){
    $.ajax({
        type: 'GET',
        url: url,
        data:data,
        dataType: 'json',
        success: function(data){
            var code = data[0];
            if(code == '200'){
                alert(success_message);
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
}

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

