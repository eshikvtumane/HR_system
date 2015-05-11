
// формирование и скачивание отчёта
$(document).on('submit', 'form#FileDownload', function(e){
console.log('fff')
    var period = document.getElementById('period').value;
    if(period == '__-__-____'){
        period = new Date();
        var date = period.getDate();
        var month = (period.getMonth() + 1);
        if(month < 10){
            month = '0' + month;
        }

        var year = period.getFullYear();
        period = date + '-' + month + '-' + year;
        console.log(period)
    }
            $.fileDownload($(this).prop('action'), {
            //preparingMessageHtml: "Подождите, отчёт формируется ...",
            //failMessageHtml: "Ошибка! Попробуйте произвести формировние отчёта позднее.",
            httpMethod: 'GET',
            data: {
                    'period': period
                    //'vacancies': JSON.stringify(vacancies)
                }
            });

        e.preventDefault();
        return;

});
