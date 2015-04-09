$(function() { 
// Resize	
function resize(){
	$('.resize-height').height(window.innerHeight - 50);
	$('.resize-width').width(window.innerWidth - 250);
	//if(window.innerWidth<=1150){$('.resize-width').css('overflow','auto');}
	
	}
$( window ).resize(function() {resize();});
resize();

	
	
 
//Add Sections
$("#newsletter-builder-area-center-frame-buttons-add").hover(
  function() {
    $("#newsletter-builder-area-center-frame-buttons-dropdown").fadeIn(200);
  }, function() {
    $("#newsletter-builder-area-center-frame-buttons-dropdown").fadeOut(200);
  }
);

$("#newsletter-builder-area-center-frame-buttons-dropdown").hover(
  function() {
    $(".newsletter-builder-area-center-frame-buttons-content").fadeIn(200);
  }, function() {
    $(".newsletter-builder-area-center-frame-buttons-content").fadeOut(200);
  }
);


$("#add-header").hover(function() {
    $(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='header']").show()
	$(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='content']").hide()
	$(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='footer']").hide()
  });
  
$("#add-content").hover(function() {
    $(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='header']").hide()
	$(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='content']").show()
	$(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='footer']").hide()
  });
  
$("#add-footer").hover(function() {
    $(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='header']").hide()
	$(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='content']").hide()
	$(".newsletter-builder-area-center-frame-buttons-content-tab[data-type='footer']").show()
  });   
  
  
  
 $(".newsletter-builder-area-center-frame-buttons-content-tab").hover(
  function() {
    $(this).append('<div class="newsletter-builder-area-center-frame-buttons-content-tab-add" style="z-index: 99999"><i class="fa fa-plus" style="z-index: 99999"></i>&nbsp; Добавить</div>');
	$('.newsletter-builder-area-center-frame-buttons-content-tab-add').click(function() {

	var $res_clone = $("#newsletter-builder-area-center-frame-content").prepend($("#newsletter-preloaded-rows .sim-row[data-id='"+$(this).parent().attr("data-id")+"']").clone());

    var draggable_classes = [
        "sim-row-header1-nav-logo",
        "sim-row-edit",
        "sim-row-header1-nav-links"
    ]
    //"sim-row-header1-nav"
    var resize_south_classes = [
        "sim-row-header1-nav",
        "sim-row-header2-nav",
        "sim-row-content1-tab",
        "sim-row-content2-left",

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
        "sim-row-content4-title sim-row-edit",
        'sim-row-content4-content sim-row-edit'
    ]

    for(var i=0; i<resize_classes.length; i++){
        $res_clone.find('[class*="' + resize_classes[i] + '"]').resizable();
    }

    for(var i=0; i<draggable_classes.length; i++){
        $res_clone.find('[class*="' + draggable_classes[i] + '"]').draggable();
    }
    for(var i=0; i<resize_south_classes.length; i++){
        $res_clone.find('[class="' + resize_south_classes[i] + '"]').resizable({
        handles: 's'
    });

    }

	hover_edit();
	perform_delete();
	perform_change_color();


	$("#newsletter-builder-area-center-frame-buttons-dropdown").fadeOut(200);
		})
  }, function() {
    $(this).children(".newsletter-builder-area-center-frame-buttons-content-tab-add").remove();
  }
); 
  
  
//Edit
function hover_edit(){


$(".sim-row-edit").hover(
  function() {
    $(this).append('<div class="sim-row-edit-hover"><i class="fa fa-pencil" style="line-height:30px;"></i></div>');
	$(".sim-row-edit-hover").click(function(e) {e.preventDefault()})
	$(".sim-row-edit-hover i").click(function(e) {
	e.preventDefault();
	big_parent = $(this).parent().parent();
	
	//edit image
	if(big_parent.attr("data-type")=='image'){
	
	
	$("#sim-edit-image .image").val(big_parent.children('img').attr("src"));
	$("#sim-edit-image").fadeIn(500);
	$("#sim-edit-image .sim-edit-box").slideDown(500);
	
	$("#sim-edit-image .sim-edit-box-buttons-save").click(function() {
	  $(this).parent().parent().parent().fadeOut(500)
	  $(this).parent().parent().slideUp(500)

	  fn = function(data){
            var code = data[0];
            if(code == '200'){
                big_parent.children('img').attr("src",data[1]);
            }
            else{
                var message = 'Произошла ошибка при загрузке изображения.';
            }
        }

        var input = document.getElementById('input_load_image');
        if (input.files && input.files[0]) {
            saveImageOnServer('input_load_image', fn);
           }
	   });

	}
	
	//edit link
	if(big_parent.attr("data-type")=='link'){

	// получаем объект кнопки
	var $div_link = big_parent.parent();

	$("#sim-edit-link .title").val(big_parent.text());
	$("#sim-edit-link .url").val(big_parent.attr("href"));
	$("#sim-edit-link").fadeIn(500);
	$("#sim-edit-link .sim-edit-box").slideDown(500);
	
	$("#sim-edit-link .sim-edit-box-buttons-save").click(function() {
	  $(this).parent().parent().parent().fadeOut(500)
	  $(this).parent().parent().slideUp(500)

	    big_parent.text($("#sim-edit-link .title").val());
		big_parent.attr("href",$("#sim-edit-link .url").val());
		big_parent.css("color",$("#inp_color_text_link").val());
        $div_link.css("background-color",$("#inp_color_btn_link").val());
		});

	}
	
	//edit title
	
	if(big_parent.attr("data-type")=='title'){
	
	$("#sim-edit-title .title").val(big_parent.text());
	$("#sim-edit-title").fadeIn(500);
	$("#sim-edit-title .sim-edit-box").slideDown(500);


	tinyMCE.get('editor').setContent(big_parent.html());
	
	$("#sim-edit-title .sim-edit-box-buttons-save").click(function() {
	  $(this).parent().parent().parent().fadeOut(500)
	  $(this).parent().parent().slideUp(500)

        big_parent.html(tinyMCE.get('editor').getContent());
        big_parent.resizable('destroy');
        big_parent.resizable();
        big_parent.parent().remove('.sim-row-edit-hover');
		});

	}
	
	//edit text
	if(big_parent.attr("data-type")=='text'){
	
	$("#sim-edit-text .text").val(big_parent.text());
	$("#sim-edit-text").fadeIn(500);
	$("#sim-edit-text .sim-edit-box").slideDown(500);

    //CKEDITOR.instances['editor2'].setData();
    tinyMCE.activeEditor.setContent(big_parent.html());
    $("#sim-edit-text .text").val();
	
	$("#sim-edit-text .sim-edit-box-buttons-save").click(function() {
	  $(this).parent().parent().parent().fadeOut(500)
	  $(this).parent().parent().slideUp(500)

	    big_parent.html(tinyMCE.get('editor2').getContent());

        big_parent.remove('.sim-row-edit-hover');

        big_parent.resizable('destroy');
        big_parent.resizable();
		});

	}
	
	//edit icon
	if(big_parent.attr("data-type")=='icon'){
	
	
	$("#sim-edit-icon").fadeIn(500);
	$("#sim-edit-icon .sim-edit-box").slideDown(500);
	
	$("#sim-edit-icon i").click(function() {
	  $(this).parent().parent().parent().parent().fadeOut(500)
	  $(this).parent().parent().parent().slideUp(500)
	   
	    big_parent.children('i').attr('class',$(this).attr('class'));

		});

	}//
	
	});
  }, function() {
    $(this).children(".sim-row-edit-hover").remove();
  }
);
}
hover_edit();



//close edit
$(".sim-edit-box-buttons-cancel").click(function() {
  $(this).parent().parent().parent().fadeOut(500)
   $(this).parent().parent().slideUp(500)
});
   


//Drag & Drop
$("#newsletter-builder-area-center-frame-content").sortable({
  revert: true
});
	

$(".sim-row").draggable({
      connectToSortable: "#newsletter-builder-area-center-frame-content",
      //helper: "clone",
      revert: "invalid",
	  handle: ".sim-row-move"
});



//Delete and palette
function add_delete(){
	$(".sim-row").append('<div class="sim-row-delete"><i class="fa fa-times" ></i></div>');
	$(".sim-row").append('<div class="sim-row-palette"><input type="color" class="bg_block_color" value="#FFFFFF"></i></div>');
	$(".sim-row").append('<div class="sim-row-palette"><input type="color" class="bg_block_color" value="#FFFFFF"></i></div>');
	}
add_delete();

// удаление блока
function perform_delete(){
    $(".sim-row-delete").click(function() {
      $(this).parent().remove();
    });
}
perform_delete();

function perform_change_color(){
    $(".bg_block_color").change(function() {
      $(this).parent().parent().find('[class*="sim-row-header"]').css('background-color', $(this).val());
      $(this).parent().parent().find('[class*="sim-row-content"]').css('background-color', $(this).val());
    });
}

perform_change_color();

// Скачивание шаблона
 $("#newsletter-builder-sidebar-buttons-abutton").click(function(){
	 
	$("#newsletter-preloaded-export").html($("#newsletter-builder-area-center-frame-content").html());
	$("#newsletter-preloaded-export .sim-row-delete").remove();
	$("#newsletter-preloaded-export .sim-row-palette").remove();
	$("#newsletter-preloaded-export .sim-row").removeClass("ui-draggable");
	$("#newsletter-preloaded-export .sim-row-edit").removeAttr("data-type");
	$("#newsletter-preloaded-export .sim-row-edit").removeClass("sim-row-edit");
	
	export_content = $("#newsletter-preloaded-export").html();
	
	$("#export-textarea").val(export_content)
	$( "#export-form" ).submit();
	$("#export-textarea").val(' ');
	 
});
	 
	 
// Экспорт шаблона
$("#newsletter-builder-sidebar-buttons-bbutton").click(function(){
	
	$("#sim-edit-export").fadeIn(500);
	$("#sim-edit-export .sim-edit-box").slideDown(500);
	
	$("#newsletter-preloaded-export").html($("#newsletter-builder-area-center-frame-content").html());
	$("#newsletter-preloaded-export .sim-row-delete").remove();
	$("#newsletter-preloaded-export .sim-row-palette").remove();
	$("#newsletter-preloaded-export .sim-row").removeClass("ui-draggable");
	$("#newsletter-preloaded-export .sim-row-edit").removeAttr("data-type");
	$("#newsletter-preloaded-export .sim-row-edit").removeClass("sim-row-edit");

	$("#newsletter-preloaded-export").removeClass("resize");
	
	preload_export_html = $("#newsletter-preloaded-export").html();

	var bg_style = '';

    // bg_url - глобальная переменная из constructor_init.js
    if(bg_url){
        bg_style = 'background-image:' + bg_url;
    }
    else{
        email_bg_color = $('#email_bg_color').val();
        bg_style = 'background-color:' + email_bg_color;
    }

	var sim_wrapper_style = 'style="float: left;height: auto;width: 100%;margin: 0px;padding-top: 50px;padding-right: 0px;padding-bottom: 50px;padding-left: 0px;' + bg_style + '"'
export_content = '<div id="sim-wrapper" ' + sim_wrapper_style + '><div id="sim-wrapper-newsletter">'+preload_export_html+'</div></div>';
	$("#sim-edit-export .text").val(export_content);

	
	$("#newsletter-preloaded-export").html(' ');
	
	});




});