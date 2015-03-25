$(document).ready(function(){
    $('#id_sex').change(function(){
        var val = $(this).val();
        var img = document.getElementById('gender_img');

        if(val == '1'){
            img.src = '/media/gender/male.png';
        }
        else{
            img.src = '/media/gender/female.png';
        }

    });
})