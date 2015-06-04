// подсказки городов и улиц от dadata.ru
$("#fullname").suggestions({
        serviceUrl: "https://dadata.ru/api/v2",
        token: "3a41fe0db57931afae7e19c0e746924d61f8d202",
        autoSelectFirst: true,
        type: "ADDRESS",
        count: 5,
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function(suggestion) {
            console.log(suggestion);
            $('[name="city"]').val(suggestion['data']['city']);
            $('[name="street"]').val(suggestion['data']['street']);
            $('[name="building"]').val(suggestion['data']['house']);
        }
    });