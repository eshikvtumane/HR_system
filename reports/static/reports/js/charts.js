$(function () {

    $('#tabs').tabs();

    drawVacanciesDistributionChart();

});


function drawVacanciesDistributionChart(){

     $.ajax({
            type: 'GET',
            url: '/reports/get_vacancies_to_position_distribution/',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                  console.log(data);
                  $('#vacancies_distribution').highcharts({
                       chart: {
                            plotBackgroundColor: null,
                            plotBorderWidth: null,
                            plotShadow: false
                        },
                        title: {
                            text: ''
                        },
                        tooltip: {
                            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                    style: {
                                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                    }
                                }
                            }
                        },
                        series: [{
                            type: 'pie',
                            name: 'Browser share',
                            data: data

                        }]
                    });
            },
            error: function(data) {
               console.log("Ошибка при пострении графика!")
            }
        });

}



function drawVacanciesDistributionChart(){

     $.ajax({
            type: 'GET',
            url: '/reports/get_vacancies_to_position_distribution/',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                  console.log(data);
                  $('#vacancies_distribution').highcharts({
                       chart: {
                            plotBackgroundColor: null,
                            plotBorderWidth: null,
                            plotShadow: false
                        },
                        title: {
                            text: ''
                        },
                        tooltip: {
                            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                    style: {
                                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                    }
                                }
                            }
                        },
                        series: [{
                            type: 'pie',
                            name: 'Browser share',
                            data: data

                        }]
                    });
            },
            error: function(data) {
               console.log("Ошибка при пострении графика!")
            }
        });

}
