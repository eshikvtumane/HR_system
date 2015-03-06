// Добавление эскиза загруженного изображения на страницу
var imageLoader = document.getElementById('imageLoader');
    imageLoader.addEventListener('change', handleImage, false);
var canvas = document.getElementById('imageCanvas');
var ctx = canvas.getContext('2d');


function handleImage(e){
    width = 300;
    var reader = new FileReader();
    reader.onload = function(event){
        var img = new Image();
        img.onload = function(){
        console.log(img.width)
        //
            img_width = img.width; // длина картинки
            img_height = img.height; // ширина картинки

            // вычисление ширины для картинки
            height = (img_height * width) / img_width;


            img.width = width;
            img.height = height;

            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img,0,0,img.width, img.height);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(e.target.files[0]);
}
