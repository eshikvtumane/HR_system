$(document).ready(function(){
    $('.easy_modal').easyModal();
    $('.easy-modal-open').click(function(e) {
        var target = $(this).attr('href');
        $(target).trigger('openModal');
        e.preventDefault();
    });
    $('.easy-modal-close').click(function(e) {
            $('.easy_modal').trigger('closeModal');
    });

    $('#hot_applicant_add').click(function(){
        $('#modal1').trigger('openModal');
        $.ajax({
            type: 'GET',
            url: '/applicants/position_source_get/',
            dataType: 'json',
            success: function(data){
                var code = data[0];
                if(code == '200'){
                    fillingSelect('', data[1]['positions']);
                    fillingSelect('', data[1]['sources']);
                }
                else{
                    console.log(data[1])
                }
            },
            error: function(){
                alert('Ошибка загрузки должностей и источников');
            }
        });

    });
    $('#modal1').trigger('closeModal');
});

function fillingSelect(select_id, data){
    var select = document.getElementById(select_id);

    data.forEach(function(item, i, arr){
        var options = document.createElement('option');
        option.value = item['id'];
        option.text = item['name'];
        select.appendChild(option);
    });

    return;

}