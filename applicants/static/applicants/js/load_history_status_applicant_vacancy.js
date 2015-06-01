$(document).ready(function(){
    var div_id = 'divHistoryStatusApplicantVacancy';
    var div_result = document.getElementById(div_id);


    $('.status_candidate_vacancy').click(function(e){

        ajaxLoader(div_id);
        //console.log($(this).parent().find('.vacancy-id').val())
        //console.log($)
        var $id=$(this).parent().parent().parent().children('.app-vacancy-id').val();
        //var $id=$(this).val();

        var table = document.createElement('table');
        var header_tr = document.createElement('tr');
        var header_arr = ['Дата изменения', 'Статус', 'Примечание']

        var header_len = header_arr.length;
        for(var i=0; i<header_len; i++){
            var th = document.createElement('th');
            th.appendChild(document.createTextNode(header_arr[i]));
            header_tr.appendChild(th);
        }

        table.setAttribute('class', 'table');
        table.setAttribute('id', 'tbl_statuses');
        table.appendChild(header_tr);

        div_result.innerHTML = '';
        div_result.appendChild(table);

        var button_save_status = document.createElement('button');
        button_save_status.setAttribute('class', "btn btn-success save-status");
        button_save_status.setAttribute('value', $id);
        button_save_status.setAttribute('onclick', 'saveStatus(this);');
        button_save_status.appendChild(document.createTextNode('Добавить статус'));

        document.getElementById('divBtnSaveStatus').innerHTML = '';
        document.getElementById('divBtnSaveStatus').appendChild(button_save_status);

        $.ajax({
            type: 'GET',
            url: '/applicants/status_add/',
            data: {
                'applicant_vacancy': $id
            },
            dataType: 'json',
            success: function(data){
                if(data[0] == '200'){
                    console.log('OK');
                    if(data[1]){
                        var statuses = data[1];
                        var status_len = statuses.length;
                        for(var i=0; i<status_len; i++){
                            var tr = document.createElement('tr');


                            for (var key in statuses[i]) {
                                var td = document.createElement('td');
                                td.appendChild(document.createTextNode(statuses[i][key]));
                                tr.appendChild(td);
                            }
                            table.appendChild(tr);
                        }

                    }
                }
                else{
                    console.log('Fail');
                }
            }
        });
    });


    $('.save-status').click(function(){

    });
});

function saveStatus(obj){
    var tbl = document.getElementById('tbl_statuses');
    var select_status = document.getElementById('applicant_vacancy_status');
     var status_id = select_status.value;
     var user_id = document.getElementById('user_id').value;
     var $note = $('#textarea_note');

     var control = $(select_status)[0].selectize;
    if(status_id){
        $.ajax({
            type: 'POST',
            url: '/applicants/status_add/',
            data: {
                'applicant_vacancy': obj.value,
                'status': control.getValue(),
                'user_id': user_id,
                'note': $note.val()
            },
            dataType: 'json',
            success: function(data){
            console.log(data[0])
                if(data[0] == '200'){
                    var tr = createTR();

                    var td_date = createTD();
                    var td_status = createTD();
                    var td_note = createTD();

                    td_date.appendChild(document.createTextNode(data[1]));
                    td_status.appendChild(document.createTextNode(select_status.options[select_status.selectedIndex].text));
                    td_note.appendChild(document.createTextNode($note.val()));

                    tr.appendChild(td_date);
                    tr.appendChild(td_status);
                    tr.appendChild(td_note);

                    tbl.appendChild(tr);


                    $note.val('');
                    control.clear();
                }
                else{
                    console.log('Fail');
                }
            }
        });
    }
}

function sendDataAjax(url, data, fn){
    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        dataType: 'json',
        success: fn
    })
}

function createTR(){
    return document.createElement('tr');
}
function createTD(){
       return document.createElement('td');
}