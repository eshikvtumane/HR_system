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

    colorpickerClassInit();

    $('.bg-color').change(function(){
        var color = $(this).val();
        if(color){
            $('#newsletter-builder-area').css('background', '#' + color);
        }
    });


    tinymce.init({
        height: 250,
        selector: "textarea#editor,textarea#editor2",
        theme_advanced_resize_vertical: false,
        language : "ru",
        fontsize_formats: "8pt 10pt 12pt 14pt 18pt 24pt 36pt",
        relative_urls : false,
        remove_script_host : false,
        convert_urls : true,
        theme_advanced_link_targets : "_blank",
        extended_valid_elements : "a[href|target=_blank]",
        plugins: [
             "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
             "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
             "save table contextmenu directionality emoticons template paste textcolor placeholder videothumbnail"
       ],
        toolbar: [
            "undo redo | styleselect | bold italic | link image | imageupload | videothumbnail",
            "alignleft aligncenter alignright | forecolor backcolor | fontselect |  fontsizeselect | emoticons"
        ],
        file_browser_callback : function(field_name, url, type, win){
            if(type=='image'){
                $('#my_form input').click();
            }
        },
        setup: function(editor){
            editor.on('ObjectResized', function(e){
                console.log(e);
            });
        }
     });


    $('#upload_image').on('change', function(){
        $('#modal2').trigger('openModal');
        var fd = new FormData();
        fd.append('image', document.getElementById('upload_image').files[0]);

        $.ajax({
            type: 'POST',
            url: '/email_constructor/save_tinymce_img/',
            data: fd,
            dataType: 'json',

            processData: false,
            contentType: false,
            success: function(data){
                var code = data[0];
                
                if(code == '200'){
                    $('.mce-placeholder').val(data[1]);
                }
                else{
                    alert('Ошибка загрузки. ' + data[1]);
                }
                $('#modal2').trigger('closeModal');
            }
        });
    });

    $('.resize').resizable({
        handles: 's'
    });

    $('.draggable-block').draggable();
    $('.block-resize').resizable();

    // смена фона у письма
    $('#inp_bg_color').change(function(){
        $('#newsletter-builder-area').css('background', $(this).val());
        bg_url = 'background-color: ' + $(this).val() + ';';
    });

    // установить в качестве фона письма изображение
    $('#inp_bg_img').change(function(){
        var img = 'inp_bg_img';
        $('#div_load_bg_message').html('Идёт загрузка ...');
        if(img){
            var fn = function(data){
               var code = data[0];
                if(code == '200'){
                    var url = 'url(' + data[1] + ')';
                    console.log(url)
                    $('#newsletter-builder-area').css('background-image', url);
                    bg_url = 'background-image: ' + url;

                    console.log($('#newsletter-builder-area').css('background-image'))
                    $('#div_load_bg_message').html('');
                }
            };

            saveImageOnServer(img, fn);
        }
        $('#div_load_bg_message').html('');
    });

    // сохранение шаблона
    $('#btn_save_template').click(function(){
            var name = $('#template_name').val();
            var html = $('#newsletter-builder-area-center-frame-content').html();

            $.ajax({
                type: 'POST',
                url: '/email_constructor/save_template/',
                data: {
                    'name': name,
                    'html': html
                },
                dataType: 'json',
                success: function(data){
                    var code = data[0];
                    if(code == '200'){
                        var cells = '<td width="80%">' + name + '</td>' + '<td><button class="get-template-html" value="' + data[1] + '">Выбрать</button></td>'
                        $("#tbl_templates tr:last").after('<tr>' + cells + '</tr>');
                        alert('Шаблон успешно добавлен');
                    }
                    else{
                        alert('Произошла ошибка при добавлении шаблона');
                    }

                }
            });
    });


    // загрузка выбранного шаблона
    $('.load-template').click(function(){
        var template_id = $(this).val();

        $.ajax({
            type: 'GET',
            url: '/email_constructor/load_template/',
            data: { 'id': template_id },
            success: function(data){
                var code = data[0];
                if(code == '200'){
                    var $template = $('#newsletter-builder-area-center-frame-content').html(data[1]);
                    colorpickerInit($template);


                    var draggable_classes = [
                        "sim-row-header1-nav-logo",
                        "sim-row-edit",
                        "sim-row-header1-nav-links"
                    ]
                    //"sim-row-header1-nav"
                    var resize_south_classes = [
                        "sim-row-header1",
                        "sim-row-header2-nav"

                    ]

                    for(var i=1; i < 19; i++){
                        resize_south_classes.push('sim-row-content' + i.toString());
                    }

                    var resize_classes = [
                        "sim-row-header1-nav-links",
                        "sim-row-header1-slider-left-text",
                        "sim-row-edit",
                        "sim-row-header2-nav-logo",
                        "sim-row-content2-right-text",
                        "sim-row-content4-title",
                        "sim-row-content2-right-text",
                        "sim-row-content2-right-text sim-row-edit ui-draggable",
                        "sim-row-content3",
                        'sim-row-content3-center-tab-image',
                        "sim-row-content4-title",
                        'sim-row-content4-content'
                    ]



                    for(var i=0; i<resize_south_classes.length; i++){
                        console.log(resize_south_classes[i])
                        $('#newsletter-builder-area-center-frame-content [class*="' + resize_south_classes[i] + '"]').find('.ui-resizable-handle').remove();
                        $('#newsletter-builder-area-center-frame-content [class*="' + resize_south_classes[i] + '"]').resizable({
                            handles: 's'
                        });
                    }

                    for(var i=0; i<resize_classes.length; i++){
                        $template.find('[class*="' + resize_classes[i] + '"]').resizable();
                    }

                    for(var i=0; i<draggable_classes.length; i++){
                        $template.find('[class*="' + draggable_classes[i] + '"]').draggable();
                    }

                    /*$('#newsletter-builder-area-center-frame-content').find('div').each(function (index) {
                            console.log($(this).children('div:first div'))
                            $(this).children('div:first div').resizable({
                                handles: 's'
                            });
                        });*/
                    /*for(var i=0; i<resize_south_classes.length;i++){
                        $('#newsletter-builder-area-center-frame-content .sim-row').find('div').each(function (index) {
                            $(this).resizable();
                        });
                    }*/
                    

                    hover_edit();
                    perform_delete();
                    perform_change_color();

                    $('.easy_modal').trigger('closeModal');
                    console.log('Шаблон успешно скачан');
                }
                else{
                    alert('Ошибка при загрузке');
                }
            }
        });
    });
});

var bg_url = 'background-color: #C3CCD5';

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


// функция сохранения шаблона
function saveTemplates(){
    var $name = $('#template_name').val();

    $("#newsletter-preloaded-export").html($("#newsletter-builder-area-center-frame-content").html());
    $("#newsletter-preloaded-export .sim-row-delete").remove();
    $("#newsletter-preloaded-export .sim-row-palette").remove();

    var id= document.getElementById('newsletter-preloaded-export');
    var class_remove = ' resize';
    var d;
    d=document.getElementById(id);
    d.className=d.className.replace(myClassName,"");

    active.classList.remove("resize");

    //$(".sim-row div .resize").removeClass('resize');
    $(".sim-row").removeClass("ui-resizable");
    $(".sim-row").removeClass("ui-draggable");




    $.ajax({
        type: 'POST',
        url: '/email_constructor/save_template/',
        data: {
            'name': $name,
            'html': $html
        },
        dataType: 'json',
        success: function(data){
            var code = data[0];
            if(code == '200'){
                var cells = '<td width="80%">' + name + '</td>' + '<td><button class="get-template-html" value="' + data[1] + '">Выбрать</button></td>'
                $("#tbl_templates tr:last").after('<tr>' + cells + '</tr>');
                alert('Шаблон успешно добавлен');
            }
            else{
                alert('Произошла ошибка при добавлении шаблона');
            }

        }
    });
}

function colorpickerInit(el){
    colorpicker(el.find('.color'));
}

function colorpickerClassInit(){
    colorpicker($('.color'));
}

function colorpicker(el){
    el.change(function(){
        var color = $(this).val();
        if(color){
            console.log($(this).parent().parent().children().attr('class'))
            console.log(color)
            $(this).parent().parent().children().css('background-color', '#' + color);
        }
    });
}

hover_edit();
add_delete();

perform_change_color();
