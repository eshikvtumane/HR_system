$(document).ready(function(){
    tinymce.init({
        selector: "textarea#editor2",
        language : "ru",
        fontsize_formats: "8pt 10pt 12pt 14pt 18pt 24pt 36pt",
        plugins: [
             "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
             "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
             "save table contextmenu directionality emoticons template paste textcolor"
       ],
        toolbar: [
            "undo redo | styleselect | bold italic | link image",
            "alignleft aligncenter alignright | forecolor backcolor | fontselect |  fontsizeselect"
        ]
     });

    $('.resize').resizable({
        handles: 's'
    });

    $('.draggable-block').draggable();
    $('.block-resize').resizable();

    // смена фона у письма
    $('#inp_bg_color').change(function(){
        $('#newsletter-builder-area').css('background', $(this).val());
    });

    // установить в качестве фона письма изображение
    $('#inp_bg_img').change(function(){
        var img = 'inp_bg_img';
        if(img){
            var fn = function(data){
               var code = data[0];
                if(code == '200'){
                    var url = 'url(' + data[1] + ')';
                    $('#newsletter-builder-area').css('background-image', url);
                    bg_url = url;
                }
            };

            saveImageOnServer(img, fn);
        }
    });
});

var bg_url = '';

// функция сохранения выбранного изображения на сервере
function saveImageOnServer(img, fn){
    img = document.getElementById(img).files[0];

    if(img){
        var form_data = new FormData();
        form_data.append('img', img);
        $.ajax({
            type: 'POST',
            url: '/email_constructor/save_img/',
            data: form_data,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: fn
        });
    }
}