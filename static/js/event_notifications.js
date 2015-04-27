// Просим у браузера разрешение показывать оповещения
// https://developer.mozilla.org/en-US/docs/Web/API/Notification/Using_Web_Notifications
window.addEventListener('load', function () {
    Notification.requestPermission(function (status) {
        // Это позволяет использовать Notification.permission для Chrome/Safari
        if (Notification.permission !== status) {
            Notification.permission = status;
        }
    });
});

// Список оповещений
var notificationsMenu = $("#notifications_menu");
//после того, как соединение установлено
swampdragon.ready(function(){

    //подписываемся на канал с оповещениями
    swampdragon.subscribe('notifications', 'notifications');

    //добавление оповещения к меню
    swampdragon.getList('notifications',{},function(context,data){
        data.forEach(function(notification){
            var li = $("<li>");
            var $messageContainer = $('<a>').attr('href','#');
            $messageContainer.html(notification.message);
            $messageContainer.appendTo(li);
            notificationsMenu.append(li);
        })
    });


//Получаем новое сообщение по каналу
swampdragon.onChannelMessage(function(channels, message) {
    // Добавляем оповещение
    addNotification((message.data));
})


});


// Добавление оповещения
function addNotification(notification) {
    // Если у нас есть разрешение на вывод оповещения в браузере, то мы можем его вывести
    if (window.Notification && Notification.permission === "granted") {
        new Notification(notification.message);
    }

    // Добавление оповещения к меню
    var li = $("<li>");
    var $messageContainer = $('<a>').attr('href','#');
    $messageContainer.html(notification.message);
    $messageContainer.appendTo(li);
    notificationsMenu.prepend(li);
    playSound('notification');

    // Удаляем лишние оповещения
    while (notificationsMenu.find("li").length > 5) {
        notificationsMenu.find("li")[5].remove();
    }
}
