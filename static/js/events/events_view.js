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
       },

       success:function(){
            $('#events_history').html("ALL GOOD!!!!")
       },

       error:function(){
              $('#events_history').html("ERROR OCCURED!!")
       }


       )


    })
})