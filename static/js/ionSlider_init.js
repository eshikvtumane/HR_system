$(document).ready(function(){
    var $range = $('#salary');
    start_input = document.getElementById('id_salary_start');
    end_input = document.getElementById('id_salary_end');
    var start = start_input.value;
    var end = end_input.value;

    sliderInit($range, start_input, end_input, 10000, 50000, 0, 200000)

    var $age = $('#age');
    start_input = document.getElementById('id_age_start');
    end_input = document.getElementById('id_age_end');
    var start = start_input.value;
    var end = end_input.value;

    sliderInit($age, start_input, end_input, 10, 60, 10, 100)
});

function sliderInit($slider, start_input, end_input, default_start, default_end, min, max){
    if(start_input.value == '' && end_input.value == ''){
        start_input.value = default_start;
        end_input.value = default_end;
    }

    $slider.ionRangeSlider({
        type: 'double',
        min: min,
        max: max,
        from: parseInt(start_input.value),
        to: parseInt(end_input.value),
        grid: true
    });

    $slider.on('change', function(){
        $this = $(this);
        from = $this.data("from");
        to = $this.data("to");

        start_input.value = from;
        end_input.value = to;
    });
}