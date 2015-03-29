$(document).ready(function(){
    $('.select-chosen').chosen({
        disable_search: true,
        single_backstroke_delete: true
    });

    $('.select-chosen-all').chosen({
        allow_single_deselect: true
    });
});