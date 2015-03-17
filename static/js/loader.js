// создание элемента img с ajax-loader
function ajaxLoader(div_id){
    var div = document.getElementById(div_id);
    var img = document.createElement('img');
    img.src = '/media/ajax-loader.gif'
    div.innerHTML = '';
    div.appendChild(img);
}