$(document).ready(function(){
    var url = '/applicants/add/';

    // validate_applicant_form.js
    validateForm(sendApplicantForm, url, fn);
});


var fn = function(data){
    var div_result = document.getElementById('create_applicant_message');
    if('200' == data[0]){
        if(data[1]){
            var url = '/applicants/view/' + data[1];
            window.location.href = url;
            div_result.innerHTML = 'Добавление прошло успешно';
        }
        else{
            div_result.innerHTML = 'Произошла ошибка при добавлении пользователя';
        }
    }
    else{
        div_result.innerHTML = 'Произошла ошибка. Пожалуйста, попробуйте повторить сохранение позднее';
        console.log(data);
    }

    document.getElementById('save_loader').innerHTML = '';
}