$(document).ready(function(){

$('.assign_event').click(function(e){
   var app_vacancy_id = $(this).parents('.btn-group').find('.app-vacancy-id').val();
   $.cookie('app_vacancy_id',app_vacancy_id,{ path: '/' });
   window.open('/events/events_calendar/','_blank');




})


})

