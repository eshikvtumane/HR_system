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


   $('.select').selectize();

   $('.select-add').selectize({
        create: true,
        createOnBlur: true,
    });

    $('.clone-wrapper').cloneya({
        limit: 3
    });



 //инициализация валидации
 // http://formvalidator.net/index.html#custom-validators
 var myLanguage = {
      errorTitle : 'Form submission failed!',
      requiredFields : 'Необходимо заполнить это поле',
      badTime : 'You have not given a correct time',
      badEmail : 'Неверно введён e-mail адрес',
      badTelephone : 'Неверный формат номера телефона',
      badSecurityAnswer : 'You have not given a correct answer to the security question',
      badDate : 'Неверный формат даты',
      lengthBadStart : 'You must give an answer between ',
      lengthBadEnd : ' characters',
      lengthTooLongStart : 'You have given an answer longer than ',
      lengthTooShortStart : 'You have given an answer shorter than ',
      notConfirmed : 'Values could not be confirmed',
      badDomain : 'Incorrect domain value',
      badUrl : 'The answer you gave was not a correct URL',
      badCustomVal : 'You gave an incorrect answer',
      badInt : 'The answer you gave was not a correct number',
      badSecurityNumber : 'Your social security number was incorrect',
      badUKVatAnswer : 'Incorrect UK VAT Number',
      badStrength : 'The password isn\'t strong enough',
      badNumberOfSelectedOptionsStart : 'You have to choose at least ',
      badNumberOfSelectedOptionsEnd : ' answers',
      badAlphaNumeric : 'The answer you gave must contain only alphanumeric characters ',
      badAlphaNumericExtra: ' and ',
      wrongFileSize : 'The file you are trying to upload is too large',
      wrongFileType : 'The file you are trying to upload is of wrong type',
      groupCheckedRangeStart : 'Please choose between ',
      groupCheckedTooFewStart : 'Please choose at least ',
      groupCheckedTooManyStart : 'Please choose a maximum of ',
      groupCheckedEnd : ' item(s)'
    };

    $.formUtils.addValidator({
      name : 'icq',
      validatorFunction : function(value, $el, config, language, $form) {
      console.log(value);
      console.log(value.length);
        if(value.length != 0){
            var reg = new RegExp('^[0-9]+$');
            result = reg.test(value);
            return result;
        }
        return true;
      },
      errorMessage : 'Номер ICQ должен состоять из цифр',
      errorMessageKey: 'badEvenNumber'
    });

    $.formUtils.addValidator({
      name : 'skype',
      validatorFunction : function(value, $el, config, language, $form) {
      login_len = value.length;
        if(login_len != 0 && (login_len > 32 || login_len < 6)){
            console.log(value);
            //var reg = new RegExp('^[0-9]+$');
            //result = reg.test(value);
            return false;
        }
        return true;
      },
      errorMessage : 'Логин Skype должен содержать от 6 до 32 символов',
      errorMessageKey: 'badEvenNumber'
    });

    // валидация отчества
    $.formUtils.addValidator({
      name : 'middle_name',
      validatorFunction : function(value, $el, config, language, $form) {
      login_len = value.length;
        if(login_len != 0){
            console.log(value);
            var reg = new RegExp('^([А-Яа-яЁё]+)$');
            result = reg.test(value);
            return result;
        }
        return true;
      },
      errorMessage : 'Отчество должно состоять из кириллических символов',
      errorMessageKey: 'badEvenNumber'
    });
  $.validate({
    language : myLanguage
  });
}

function loadCanvas() {
console.log('dffdf');
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


// заполнение select'a годами
function setYear(div){
    var start = 1900;
    var end   = new Date().getFullYear() + 10;


    var empty = 'Выберите дату';
    $('.yearpicker').append($('<option value/>').html(empty));

    for (i = end; i > 1900; i--)
    {
         $('.yearpicker').append($('<option />').val(i).html(i));
    }
}