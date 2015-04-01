$(function(){
    $('#vacancy_slct').on('change',function(){
       var vacancy_id = $(this).val();

       $.ajax({
        type: 'GET',
        url: '/events/get_vacancy_events/',
        dataType:'json',
        data:{
            'app_vacancy_id': vacancy_id
        },


       success:function(data){
            var field_names =  ['event','start','end','author','happened'];
            $('#events_table').find('tbody').empty();
            for (i=0;i<data.length;i++){
                var event = data[i];
                var $row =  $('<tr>');
                for(j=0; j < field_names.length; j++)
                {
                    if (field_names[j] == 'happened'){

                        if (event[field_names[j]]){
                            alert("true")
                            $("<td>",{

                            }).appendTo($row).append($is_happened_chk);



                        }else{
                             alert("false")
                             $("<td>",{

                            }).appendTo($row).append("<input type='checkbox'>");
                        }

                    }
                    else{
                    $('<td>',{
                       text:event[field_names[j]]
                    }).appendTo($row);
                        }

                }


              $('#events_table').find('tbody').append($row);
            };



       },

       error:function(){
              $('#events_table').find('tbody').empty();
              $('#errors_box').html("ERROR OCCURED!!")
       }


      })

      })
})