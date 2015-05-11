window.onload = function(){

fixedButton("fixed_button_update");

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

// если пользователь загружает фото
    $('#id_photo').change(function(){
        readURL();
    });

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
    $('.select-add').each(function(){
       $(this).selectize({

                 create: true,
                 createOnBlur: true

             });

    });


     $('#applicant_vacancy_status').selectize();

    $('.clone-wrapper').cloneya({
        limit: 3
    });


    //отображаем значок при смене пола
    $('#id_sex').change(function(){
        var val = $(this).val();
        var img = document.getElementById('gender_img');

        if(val == '1'){
            img.src = '/media/gender/male.png';
        }
        else{
            img.src = '/media/gender/female.png';
        }
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


// отображение выбранного изображения
function readURL(){
    var input = document.getElementById('id_photo');
    if(input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = function(e){
            $('#imagePreview').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function fixedButton(id){
    var id = '#' + id;
    if($(window).scrollTop() > 150){
            $('#update_info').addClass('fixed-button-update')
            $(id).fadeIn("slow");
        }

    $(window).scroll(function(){
    console.log(id)
        if($(window).scrollTop() > 150){
            $('#update_info').addClass('fixed-button-update')
        }
        else{
            $('#update_info').removeClass('fixed-button-update')
        }
    });
}


