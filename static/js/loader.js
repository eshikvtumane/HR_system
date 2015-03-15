// создание элемента img с ajax-loader
function ajaxLoader(div){
    var img = document.createElement('img');
    img.src = '/media/ajax-loader.gif'
    div.appendChild(img);
}