function validateForm(send_fn, url, success_fn){
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
          badDomain : 'Incorrect domain value',
          badUrl : 'The answer you gave was not a correct URL',
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
                var reg = new RegExp('^([А-Яа-яЁё -]+)$');
                result = reg.test(value);
                return result;
            }
            return true;
          },
          errorMessage : 'Отчество должно состоять из кириллических символов',
          errorMessageKey: 'badEvenNumber'
        });

        // валидация названия email
        $.formUtils.addValidator({
          name : 'custom-email',
          validatorFunction : function(value, $el, config, language, $form) {
            email_len = value.length;
            if(email_len != 0){
                var reg = new RegExp('^([А-Яа-яЁё -]+)$');
                result = reg.test(value);
                return result;
            }
            return true;
          },
          errorMessage : 'Неверно введен email',
          errorMessageKey: 'badEvenNumber'
        });

        $.validate({
        language : myLanguage,
        onSuccess : function() {
          send_fn(url, success_fn);
          return false; // Will stop the submission of the form
        }
      });
}