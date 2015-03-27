$(document).ready(function(){
    var $range = $('#salary');
    start_input = document.getElementById('id_salary_start');
    end_input = document.getElementById('id_salary_end');
    var start = start_input.value;
    var end = end_input.value;

    if(start == '' && end == ''){
        start = 10000;
        end = 50000;

        start_input.value = start;
        end_input.value = end;
    }

    $range.ionRangeSlider({
        type: 'double',
        min: 0,
        max: 200000,
        from: parseInt(start),
        to: parseInt(end),
        grid: true
    });

    $range.on('change', function(){
        $this = $(this);
        from = $this.data("from");
        to = $this.data("to");

        console.log(from)

        document.getElementById('id_salary_start').value = from;
        document.getElementById('id_salary_end').value = to;
    });
});