$(document).ready(function(){

    var $select = $('.select-vacancy').selectize({
        create: true,
        createOnBlur: true
    });


    $('#btnAddVacancy').click(function(e){
           e.preventDefault();
           addVacancy();

    });

    // изменение значений в вакансиях при изменении должности
    $('#position').change(function(){
        var position_id = document.getElementById('position').value;
        var select_vacancies = document.getElementById('vacancies');

        var div_loader = document.getElementById('loader');
        var div_message = document.getElementById('message');
        ajaxLoader('loader');
        div_message.innerHTML = 'Загрузка вакансий';


// выборка вакансий по выбранной должности
        $.ajax({
            type: 'GET',
            url: '/applicants/vacancy_search/',
            data: {
                'position': position_id
            },
            dataType: 'json',
            success: function(data){
                var control = $select[0].selectize;
                control.clearOptions();

                for(var i = 0; i < data.length; i++){

                    var d = {
                        value: data[i]['value'],
                        text: data[i]['head'] + ', от ' + data[i]['date'] + ' (' + data[i]['status_name'] + ')'
                    };
                    control.addOption(d);

                }

                div_loader.innerHTML = '';
                div_message.innerHTML = 'Вакансии загружены';
            }
        });
    });


// добавление образования
    $('#btnAddEdu').click(function(){
        addEdu();
    });
});


//position_name = position.options[position.selectedIndex].text;


// добавление вакансий
var va = new WorkWithTable('tblAddingVacancy', 'vac', 'rowDelete');
var vacancies = {};
function addVacancy(){
    var val_dict = createDict(vacancies, va);
    vacancies = $.extend(vacancies, val_dict);
    console.log(vacancies);
}

// создание словаря с добавленными вакансиями
var createDict = function(vacancies, tbl_work){
    position = document.getElementById('position');
    vacancy = document.getElementById('vacancies');

    salary = document.getElementById('salary');
    suggested_salary = document.getElementById('suggested_salary');

    source = document.getElementById('source[]');

    position_id = parseInt(position.value);
    position_name = position.options[position.selectedIndex].text;
    vacancy_id = parseInt(vacancy.value);
    vacancy_name = vacancy.options[vacancy.selectedIndex].text;

    salary_sum = parseFloat(salary.value);
    suggested_salary_sum = parseFloat(suggested_salary.value);
    source_val = source.value;

    var message = document.getElementById('message');

    if(position_id && position_name && salary_sum && suggested_salary_sum && source_val){
        var arr = [
            position_name,
            vacancy_name,
            salary_sum,
            suggested_salary_sum
        ]

        tbl_work.addRecords(arr);

        var dict = {};
        dict[tbl_work.count_id.toString()] = {
                //'position': position_id,
                'vacancy': vacancy_id,
                'salary': salary_sum,
                'suggested_salary': suggested_salary_sum,
                'source': source_val
        };

        salary.value = '';
        suggested_salary.value = '';
        message.innerHTML = '';

        return dict;
    }
    else{
        message.innerHTML = 'Заполните все поля';
    }


}
// удаление вакансий
function rowDelete(id){
    vacancies = va.deleteRecords(id, vacancies);
    console.log(vacancies);
}


// добавление образования
var edu = new WorkWithTable('tblAddingEdu', 'edu', 'rowDeleteEdu');
var educations = {};
function addEdu(){
    var val_dict = createEduDict(educations, edu);
    educations   = $.extend(educations, val_dict);
    console.log(educations);
}

// создание словаря с добавленными образованиями
function createEduDict(edu, tbl_edu){
    var education   = document.getElementById('id_education');
    var edu_id      = education.value;
    var edu_name    = education.options[education.selectedIndex].text;
    var major       = document.getElementById('id_major');
    var major_id    = major.value;
    var major_name  = major.options[major.selectedIndex].text;

    var study_start = document.getElementById('id_study_start').value;
    var study_end   = document.getElementById('id_study_end').value;

    message = document.getElementById('messageEdu');

    if(edu_id != '' && major_name != '' && study_start != '' && study_end != ''){
        var arr = [
            edu_name,
            major_name,
            study_start + ' - ' + study_end,

        ]

        tbl_edu.addRecords(arr);

        var dict = {};
        dict[tbl_edu.count_id.toString()] = {
                'education': edu_id,
                //'major_name': major_name,
                'major': major_id,
                'study_start': study_start,
                'study_end': study_end
        };

        study_start.value = '';
        study_end.value = '';
        message.innerHTML = '';

        return dict;
    }
    else{
        message.innerHTML = 'Заполните все поля';
    }


}

function rowDeleteEdu(id){
    education = edu.deleteRecords(id, educations);
    console.log(educations);
}


        /* =============================================
                     Работа с таблицами
           ============================================= */

function WorkWithTable(tbl, id, del_fn){
    this.count_id = 0;
    this.array = 0;
    this.tbl_result = document.getElementById(tbl);
    this.id = id;
    this.del_fn =del_fn;
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
        btn.setAttribute('onclick', this.del_fn + '('+ this.count_id +');');

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