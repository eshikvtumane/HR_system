$(document).ready(function(){
    $('.date-picker').MonthPicker();
    var $select = $('#source').selectize();

    $('#btnAddVacancyReport').click(function(){
    console.log(111);
           addVacancyReport();
           console.log(111);
    });

    $('clearSource').click(function(){
        var control = $select[0].selectize;
        control.clearOptions();
    });

    $('#btnGenerateReport').click(function(){
        $.ajax({
            type: 'POST',
            url: '/reports/summary_statement/',
            data: {
                'period': $('#period').val(),
                'vacancies': JSON.stringify(vacancies)
            },
            dataType: 'json',
            success: function(data){
                console.log(data);

                div_loader.innerHTML = '';
                div_message.innerHTML = 'Вакансии загружены';
            }
        });
    });
});

// добавление вакансий
var va = new WorkWithTable('tblAddingVacancyReport', 'vac', 'rowDeleteReport');
var vacancies = {};
function addVacancyReport(){
    var val_dict = createDict(vacancies, va);
    vacancies = $.extend(vacancies, val_dict);
    console.log(vacancies);
}

// создание словаря с добавленными вакансиями
var createDict = function(vacancies, tbl_work){
    position = document.getElementById('position');
    vacancy = document.getElementById('vacancies');

    position_id = parseInt(position.value);
    position_name = position.options[position.selectedIndex].text;
    vacancy_id = parseInt(vacancy.value);
    vacancy_name = vacancy.options[vacancy.selectedIndex].text;

    var source_vals = $('#source').val();
    var source_texts = $('#source option:selected').map(function() {
        return $(this).text();
    }).get().join(', ');

    var message = document.getElementById('message');

    if(position_id != '' && position_name != ''){
        var arr = [
            position_name,
            vacancy_name,
            source_texts
        ]

        tbl_work.addRecords(arr);

        var dict = {};
        dict[tbl_work.count_id.toString()] = {
                //'position': position_id,
                'vacancy': vacancy_id,
                'source': source_vals
        };

        message.innerHTML = '';

        return dict;
    }
    else{
        message.innerHTML = 'Заполните все поля';
    }


}
// удаление вакансий
function rowDeleteReport(id){
    vacancies = va.deleteRecords(id, vacancies);
    console.log(vacancies);
}