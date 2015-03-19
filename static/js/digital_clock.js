$('document').ready(function(){
    $('#clock').countdown('2015/10/10', function(event) {
       var $this = $(this).html(event.strftime(''
         + '<span>%w</span> weeks '
         + '<span>%d</span> days '
         + '<span>%H</span> hr '
         + '<span>%M</span> min '
         + '<span>%S</span> sec'));
     });
    showTheTime();
});

function showTheTime() {
    now = new Date;

    current_day = showTheDay(now);

    date_time = now.getHours();
    date_time += showZeroFilled(now.getMinutes());
    date_time += showZeroFilled(now.getSeconds());

    document.getElementById('time_now').innerHTML = current_day + ' ' +date_time;

    setTimeout("showTheTime()", 1000);
}

function showTheDay(today){

    // словарь с названиями месяцев года
    var mounth_dict = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря',
    ];

    // now date
    var dd = today.getDate();
    var mm = mounth_dict[today.getMonth()]; //January is 0!
    var yyyy = today.getFullYear();

    return dd + ' ' + mm + ' ' + yyyy + ' года';
}

function showTheHours(theHour) {
     if (theHour == 0) {
          return (12);
     }
     return (theHour - 12);
}

function showZeroFilled(inValue) {
     if (inValue > 9) {
          return ":" + inValue;
     }
     return ":0" + inValue;
}