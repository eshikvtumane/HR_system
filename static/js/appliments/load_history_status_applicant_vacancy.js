$(document).ready(function(){
    $('.status_candidate_vacancy').click(function(){
        var div_id = 'divHistoryStatusApplicantVacancy';
        var div_result = document.getElementById(div_id);
        ajaxLoader(div_id);
        console.log($(this).val());

        var table = document.createElement('table');
        var header_tr = document.createElement('tr');
        var header_arr = ['Статус', 'Дата изменения']

        var header_len = header_arr.length;
        for(var i=0; i<header_len; i++){
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(header_arr[i]));
            header_tr.appendChild(td);
        }


        table.setAttribute('class', 'table');
        table.appendChild(header_tr);

        div_result.innerHTML = '';
        div_result.appendChild(table);

        var button_save_status = document.createElement('button');
        button_save_status.setAttribute('class', "btn btn-success");
        button_save_status.setAttribute('value', $(this).val());
        button_save_status.appendChild(document.createTextNode('Добавить статус'));
        console.log(button_save_status)

        document.getElementById('divStatus').appendChild(button_save_status);

    });
});

function sendDataAjax(url, data){
    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        dataType: 'json',
        success: function(data){

        }
    })
}