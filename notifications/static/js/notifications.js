
var notificationsList = document.getElementById("notifications");
swampdragon.ready(function(){

    // Список оповещений

   swampdragon.callRouter('hello', 'notifications', {value: 10}, function (context, data) {
    console.log(data);
});

swampdragon.subscribe('notifications', 'notifications');


//Получаем новое сообщение по каналу
swampdragon.onChannelMessage(function(channels, message) {
    // Добавляем оповещение
    console.log(message)
    playSound('notification_sound');
    addNotification(message.data);
})


})


// Добавление оповещения
function addNotification(notification) {
    // Если у нас есть разрешение на вывод оповещения в браузере, то мы можем его вывести
    if (window.Notification && Notification.permission === "granted") {
        new Notification(notification.message, {
            icon: 'https://cdn4.iconfinder.com/data/icons/business-management-2/256/Meeting-64.png',
            body: 'Good'
        });


    // Добавление оповещения
    var li = document.createElement("li");
    notificationsList.insertBefore(li, notificationsList.firstChild);
    li.innerHTML = notification.message;

    // Удаляем лишние оповещения
    while (notificationsList.getElementsByTagName("li").length > 5) {
        notificationsList.getElementsByTagName("li")[5].remove();
    }
}


function playSound(filename){
    //document.getElementById("sound").innerHTML='<audio autoplay="autoplay"><source src="/static/' + filename + '.mp3" type="audio/mpeg" /></audio>';
    document.getElementById(filename).play();
}
