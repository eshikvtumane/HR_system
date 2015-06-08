$(document).ready(function(){
    /*$('select').each(function(){
            $(this).selectize();
    });*/

    $('.select').each(function(){
            $(this).selectize();
    });

//инициализируем selectize.js на необходимых select элементах
    $('.select-add').each(function(){
       $(this).selectize({

                 create: true,
                 createOnBlur: true

             });

    });
});