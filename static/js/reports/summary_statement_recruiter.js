$(document).ready(function(){
    var $select = $('#source').selectize();

    $('#btnAddVacancyReport').click(function(){
           addVacancyReport();
    });

    $('#clearSource').click(function(){
        var control = $select[0].selectize;
        control.clear();
    });
});
// формирование и скачивание отчёта
$(document).on('submit', 'form#FileDownload', function(e){
    var period = document.getElementById('period').value;
    if(period != ''){
        if(document.getElementById(vacancies).value){
            $.fileDownload($(this).prop('action'), {
            //preparingMessageHtml: "Подождите, отчёт формируется ...",
            //failMessageHtml: "Ошибка! Попробуйте произвести формировние отчёта позднее.",
            httpMethod: 'GET',
            data: {
                    'period': $('#period').val(),
                    'vacancies': JSON.stringify(vacancies)
                }
            });
        }
        e.preventDefault();
        return;
    }
    document.getElementById('message').innerHTML = 'Выберите период и/или добавьте вакансии';
    e.preventDefault();
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

    var message = document.getElementById('message');
    if(position_id != '' && vacancy_id != '' && source_vals){
        var source_texts = $('#source option:selected').map(function() {
            return $(this).text();
        }).get().join(', ');

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