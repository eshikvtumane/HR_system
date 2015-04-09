window.onload = function(){
$('input:text:first').focus();

 $('input').bind("keydown", function(e) {
    var n = $("input").length;
    if (e.which == 13)
    { //Enter key
      e.preventDefault(); //Skip default behavior of the enter key
      var nextIndex = $('input').index(this) + 1;
      if(nextIndex < n)
        $('input')[nextIndex].focus();
      else
      {
        $('input')[nextIndex-1].blur();
        $('#btnSubmit').click();
      }
    }
  });


// вычисление года окончания обучения
$('#id_study_start').change(function(){

    var start = document.getElementById('id_study_start');
    var study_start = start.options[start.selectedIndex].text;


    var study_end = document.getElementById('id_study_end');
    study_end.value = parseInt(study_start) + 5;
});

// заглушка для загружаемой фотографии
    loadCanvas();
    setYear();

// инициализация datepicker
    $('#id_birthday').datetimepicker({
        lang: 'ru',
        timepicker: false,
        format: 'd-m-Y',
        mask: true
    });

    $('#id_start, #id_end').datetimepicker({
        lang: 'ru',
        timepicker: true,
        format: 'd/m/Y H:i',
        mask: true
    });



    //инициализируем selectize.js на необходимых select элементах
    $('select').each(function(){
       if ($(this).attr('class') == 'select'){
           $(this).selectize();
       }


       else if($(this).attr('class') == 'select-add'){

             $(this).selectize({

                 create: true,
                 createOnBlur: true

             });
        }
    });



    $('.clone-wrapper').cloneya({
        limit: 3
    });
};




//отлавливаем клики по пунктам меню вакансии

$('#show_vacancy_statuses').click(function(e){

    e.preventDefault();
    $('#modalVacancyStatus').modal('show');
});


$('#assign_event').click(function(e){

    e.preventDefault();
    $('#event_modal').modal('show');
});





function loadCanvas() {
    if ($('#imageCanvas').length > 0) {
        var canvas = document.getElementById('imageCanvas');
        var context = canvas.getContext('2d');
        width = 300;

        // load image from data url
        var img = new Image();
        img.onload = function(){
            img_width = img.width; // длина картинки
            img_height = img.height; // ширина картинки

            // вычисление ширины для картинки
            height = (img_height * width) / img_width;


            img.width = width;
            img.height = height;

            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img,0,0,img.width, img.height);
        }

        img.src = '/media/no_photo.gif'; //"http://placehold.it/300x150";
    }
    else{
        return;
    }
}


// заполнение select'a годами
function setYear(div){
    var start = 1900;
    var end   = new Date().getFullYear();


    var empty = 'Выберите дату';
    $('.yearpicker').append($('<option value/>').html(empty));

    for (i = end; i > 1900; i--)
    {
         $('.yearpicker').append($('<option />').val(i).html(i));
    }
}