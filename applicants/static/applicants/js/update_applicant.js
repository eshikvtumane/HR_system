$(document).ready(function(){
    var id = document.getElementById('id').value;
    var url = '/applicants/view/' + id + '/';
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

