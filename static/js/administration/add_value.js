$(document).ready(function(){
    /*
        Добавление специальности
    */
    $('#addSpec').click(function(){
        addSelect('add_speciality', 'speciality');
    });

    /*
        Удаление специальности
    */
    $('#removeSpec').click(function(){
        deleteOption('speciality');
    });

    /*
        Добавление источника
    */
    $('#addSource').click(function(){
        addSelect('add_source', 'source');
    });

    /*
        Удаление источника
    */
    $('#removeSource').click(function(){
        deleteOption('source');
    });
});


// добавление пунктов в select
function addSelect(from_value, to_add){
    // выбираем добавляемое значение из textbox
    value = document.getElementById(from_value).value;

    // создаём елемент option и присваем ему текст, который будет выводиться в select
    var option = document.createElement('option');
    option.text = value;

    // добавляем option в select
    document.getElementById(to_add).appendChild(option);
    return;
}

// удаление выбранных пунктов в select
function deleteOption(from_delete){
    $('#' + from_delete + ' > option:selected').remove();
}


// выборка значений из select
function selectToArray(select_id){
    // получение select, из которого будем получать значения
    var select_obj = document.getElementById(select_id);
    option_value = new Array();
    // получение количесва options в select
    select_length = select_obj.length;

    // добавление текста из select options в массив
    for(var i = 0; i < select_length; i++){
        option_value.push(select_obj.options[i].text);
    }

    return option_value;
}