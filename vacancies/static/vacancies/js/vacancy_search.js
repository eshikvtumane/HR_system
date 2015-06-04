$(function(){
    $('#id_search_start,#id_search_end').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y'
    });

    $('#vacancy_table').tablesorter();

});