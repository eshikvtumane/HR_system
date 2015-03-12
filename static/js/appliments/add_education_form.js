$(document).ready(function(){
    var vacancy_count = 1;
    var vacancy_arr = Array();
    $('#btnAddVacancy').click(function(){
        tbl = document.getElementById('tblAddingVacancy');

        position = document.getElementById('position');
        position_name = position.options[position.selectedIndex].text;
        vacancy = document.getElementById('vacancy').text;
        salary = document.getElementById('salary').value;
        suggested_salary = document.getElementById('suggested_salary').value;

        values = [
            position_name,
            vacancy,
            salary,
            suggested_salary
        ];


        var tr = document.createElement('tr');
        for(var i = 0; i < values.length; i++){
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(values[i]));
            tr.appendChild(td);
        }
        tbl.appendChild(tr);

    });
});

  function addVacancy(){
    var input = document.createElement('select');
    input.className = 'chosen-select';

    document.getElementById('vacancy_forms').appendChild(input);
    $('.chosen-select').chosen();
  }


    function divClone(btn, clone_from, clone_to, btn_value, div_name, btn_remove){
        div = document.getElementById(clone_from);
        clone = div.cloneNode(true);

        id = parseInt(btn_value) + 1;
        clone.id = div_name + id;
        btn.value = id.toString();
        btn_remove.value = id.toString();
        document.getElementById(clone_to).appendChild(clone);

        $('#' + clone_to).find('select').chosen();

        return;
    }