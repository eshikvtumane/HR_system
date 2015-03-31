$(function(){
    $('#vacancy_slct').on('change',function(){
       var $vacancy_id = this.val();
       $.ajax({
        type: 'GET',
        url: '/events/get_vacancy_events/',
        dataType:'json',
        data:{
            'app_vacancy_id'
        }
       })


    })
})