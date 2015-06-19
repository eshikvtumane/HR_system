// сохранение данных
function sendApplicantForm(url, fn){
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


        //var url = '/applicants/add/';
        $.ajax({
            type:'POST',
            url: url,
            data: fd,
            processData: false,
            contentType: false,
            success: fn
        });
        return false;
   //});
}