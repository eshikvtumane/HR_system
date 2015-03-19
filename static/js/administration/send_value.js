$(document).ready(function(){
// сохранение списка введённых специальностей
    $('#saveSpec').click(function(){
        saveMajor(
            'speciality',
            'speciality[]',
            '/administration/ajax_spec/',
            'result_spec_list',
            'Нет добавленных специальностей'
            );
    });


// сохранение списка специальностей их файла
    $('#btnAddSpec').click(function(){
        saveMajor(
            'spec[]',
            'speciality[]',
            '/administration/ajax_spec/',
            'result_load_spec_file',
            'Нет добавленных файлов'
        );
    });

// сохранение списка введённых источников
    $('#btnSaveSource').click(function(){
    console.log('hhh');
        saveMajor(
            'source',
            'source[]',
            '/administration/ajax_source_add/',
            'result_source_list',
            'Нет добавленных источников'
            );
    });


// сохранение списка специальностей их файла
    $('#btnAddSource').click(function(){
        saveMajor(
            'source_file',
            'source[]',
            '/administration/ajax_source_add/',
            'result_load_source_file',
            'Нет добавленных файлов'
        );
    });
});

/* сохранение специальностей
    from_elem - id элемента, откуда будут браться значения для добавления в БД
    post_key - ключ, который будет содержать пересылаемые файлы или массивы
    url - куда будем отправлять значения
    result_block - обновление статуса
    empty_msg - сообщение о пустом
    fn - переданная функция (выполнение передачи файла или массива)
*/
function saveMajor(from_elem, post_key, url, result_block, empty_msg){
    // изменение статуса
    img = ajaxLoader();
    //добавление ajax loader
    div_result = document.getElementById(result_block);
    div_result.innerHTML = '';
    div_result.appendChild(img);
    //-------------------------
    // узнаём тип элемента
    type_elem = document.getElementById(from_elem).type;
    result = Object();
    // возвращаем FormData с значениями из select
    if(type_elem == 'select-multiple'){
        result = saveTextFunction(from_elem, post_key);
    }
    // возвращаем FormData с выбранным файлом
    else if(type_elem == 'file'){
        result = saveFileFunction(from_elem, post_key);
    }
    // Если элемент не является выше перечисленными типами, то выходим из функции
    else{
        return;
    }
    // получение FormData с добавленным значением в зависимости от переданной функции
    // если функция возвращает false, то передачи запроса на сервер не происходит
    if(result != false){
        ajaxPostFD(
                url,
                result
            );
    }
    else{
        div_result.innerHTML = empty_msg;
    }
}

// отправка значений из select options
var saveTextFunction = function(from_elem, post_key){
    // копирование текста из select  в массив
    console.log(document.getElementById(from_elem).type);
    var result = selectToArray(from_elem)
    // получаем длину массива
    res_len = result.length;
    // если значений в массиве нет, то функция возвращает false
    if(res_len != 0){
        var fd = new FormData();
        for(var i = 0; i < res_len; i++){
            fd.append(post_key, result[i])
        }
        return fd;
    }
    return false;
}

// отправка файла с значениями
var saveFileFunction = function(from_elem, post_key){
    file = document.getElementById(from_elem);
    // проверка: выбрал ли пользователь файл; если нет - функция возвращает false
    if(file.value != ''){
        // добавление файла в FormData для дальнейшей передачи на сервер
        var fd = new FormData();
        fd.append(post_key, file.files[0]);
        return fd;
    }
    return false;
}


// отправка formdata через ajax post
function ajaxPostFD(url, data){
    $.ajax({
        type:'POST',
        url: url,
        data: data,
        processData: false,
        contentType: false,
        success: function(data){
            if(data == '200'){
                div_result.innerHTML = 'Добавление прошло успешно';
            }
            else{
                div_result.innerHTML = 'Произошла ошибка. Пожалуйста, попробуйте повторить сохранение позднее';
                console.log(data);
            }
        }
    });
}

// создание элемента img с ajax-loader
function ajaxLoader(){
    var img = document.createElement('img');
    img.src = '/media/ajax-loader.gif'
    return img
}
