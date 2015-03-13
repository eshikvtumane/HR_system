$(document).ready(function(){

    $('#btnAddVacancy').click(function(){
           addVacancy();
    });

    // изменение значений в вакансиях при изменении должности
    $('#position').change(function(){
        var position_id = document.getElementById('position').value;
        var select_vacancies = document.getElementById('vacancies');

        console.log('Start');
// выборка вакансий по выбранной должности
        $.ajax({
            type: 'GET',
            url: '',
            data: {
                'position': position_id
            },
            success: function(data){
                for(var i = 0; i < data.length; i++){
                    var option = document.createElement('option');
                    option.value = data[i]['id'];
                    option.text = data[i]['name'] + ' от ' + data[i]['post_date'];

                    select_vacancies.appendChild(option);
                }

console.log('End');
            }
        });
    });
});


//position_name = position.options[position.selectedIndex].text;



var va = new WorkWithTable('tblAddingVacancy', 'vac');
var vacancies = {};
function addVacancy(){
    var val_dict = createDict(vacancies, va);
    vacancies = $.extend(vacancies, val_dict);
    console.log(vacancies);
}

var createDict = function(vacancies, tbl_work){
    position = document.getElementById('position');
    //vacancy_id = document.getElementById('vacancy').value;
    salary = document.getElementById('salary');
    suggested_salary = document.getElementById('suggested_salary');

    position_id = position.value;
    position_name = position.options[position.selectedIndex].text;
    salary_sum = salary.value;
    suggested_salary_sum = suggested_salary.value;

    var arr = [
        position_name,
        //vacancy_id,
        salary_sum,
        suggested_salary_sum
    ]

    tbl_work.addRecords(arr);

    var dict = {};
    dict[tbl_work.count_id.toString()] = {
            'position': position_id,
            //'vacancy': vacancy_id,
            'salary': salary_sum,
            'suggested_salary': suggested_salary_sum
    };

    salary.value = '';
    suggested_salary.value = '';

    return dict;
}

function rowDelete(id){
    vacancies = va.deleteRecords(id, vacancies);
    console.log(vacancies);
}


        /* =============================================
                     Работа с таблицами
           ============================================= */

function WorkWithTable(tbl, id){
    this.count_id = 0;
    this.array = 0;
    this.tbl_result = document.getElementById(tbl);
    this.id = id;
};
// создание и добавление в таблицу новой строки
WorkWithTable.prototype.addRecords = function(values){
    this.count_id += 1;
    var tr = document.createElement('tr');
    tr.id = this.id + String(this.count_id);
    for(var i = 0; i < values.length; i++){
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(values[i]));
        tr.appendChild(td);
    }

    // кнопка удаления записи
    var btn = document.createElement('button');
    btn.innerHTML = 'Удалить';
    btn.setAttribute('class', 'btn btn-danger');
    btn.setAttribute('onclick', 'rowDelete('+ this.count_id +');');

    var td = document.createElement('td')
    td.appendChild(btn);
    tr.appendChild(td);

    this.tbl_result.appendChild(tr);
};
// удаление записи
WorkWithTable.prototype.deleteRecords = function(id, vacancies){
    this.tbl_result.removeChild(document.getElementById(this.id + id.toString()));
    delete vacancies[id.toString()];
    return vacancies;
};