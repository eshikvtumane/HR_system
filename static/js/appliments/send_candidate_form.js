$(document).ready(function(event){
    $('#applicant_form').submit(function(event){
        var elements = document.forms['applicant_form'].elements;
        var fd = new FormData();

        for(var i=0; i<elements.length; i++){
            var elem_name = elements[i].name;
            if(elem_name != ''){
                if(elements[i].type == 'file'){
                    fd.append(elements[i].name, elements[i].files[0]);
                }
                else{
                    fd.append(elements[i].name, elements[i].value);
                }

                console.log(elements[i].type + ' ' + elements[i].name + ' ' + elements[i].value)
            }
        }

        var div_result = document.getElementById('create_applicant_message');
        var url = '/applicants/add/';

        $.ajax({
            type:'POST',
            url: url,
            data: fd,
            processData: false,
            contentType: false,
            success: function(data){
                if(data == '200'){
                    div_result.innerHTML = 'Добавление прошло успешно';
                }
                else{
                    div_result.innerHTML = 'Произошла ошибка. Пожалуйста, попробуйте повторить сохранение позднее';
                    console.log(data);
                }
            }
        });
        return false;
   });
});


function sendApplicantForm(){

}