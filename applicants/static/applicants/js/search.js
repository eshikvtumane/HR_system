$(document).ready(function(){
    var $age_checked = $('#id_age_add');
    var $age_slider = $('#select_age');
    checkedValue($age_checked, $age_slider);

    var $salary_checked = $('#id_salary_add');
    var $salary_slider = $('#select_salary');
    checkedValue($salary_checked, $salary_slider);

    $age_checked.click(function(){
        checkedValue($age_checked, $age_slider);
    });

    $salary_checked.click(function(){
        checkedValue($salary_checked, $salary_slider);
    });
});

function checkedValue($el, $el_select){
    if($el.prop('checked')){
        $el_select.show();
    }
    else{
        $el_select.hide();
    }
}