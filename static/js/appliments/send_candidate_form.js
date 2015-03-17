// сохранение данных
$(document).ready(function(event){

});

function fff(){
    console.log(vacancies);
    console.log(JSON.stringify(vacancies));
}


function sendApplicantForm(){
    //$('#applicant_form').submit(function(event){

        var div_result = document.getElementById('create_applicant_message');
        div_result.innerHTML = '';

        ajaxLoader('save_loader');

        var elements = document.forms['applicant_form'].elements;
        var fd = new FormData();

//
        for(var i=0; i<elements.length; i++){
            var elem_name = elements[i].name;
            if(elem_name != ''){
                if(elements[i].type == 'file'){
                    fd.append(elements[i].name, elements[i].files[0]);
                }
                else{
                    fd.append(elements[i].name, elements[i].value);
                }
            }
        }

        // добавление выбранных ваканий
        fd.append('vacancies', JSON.stringify(vacancies));
        // добавление образований
        fd.append('educations', JSON.stringify(educations))


        var url = '/applicants/add/';

        $.ajax({
            type:'POST',
            url: url,
            data: fd,
            processData: false,
            contentType: false,
            success: function(data){
                if('200' == data[0]){
                    window.location.href = '/';
                    div_result.innerHTML = 'Добавление прошло успешно';
                }
                else{
                    div_result.innerHTML = 'Произошла ошибка. Пожалуйста, попробуйте повторить сохранение позднее';
                    console.log(data);
                }

                document.getElementById('save_loader').innerHTML = '';

            }
        });
        return false;
   //});
}