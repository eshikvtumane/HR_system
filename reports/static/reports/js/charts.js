$(function () {

    $('#tabs').tabs();

    drawVacanciesDistributionChart();

    $('#tab_position_avg_salary').on('click',function(){
         drawPositionAvgSalaryChart();
    })


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
                            name: 'Доля вакансий',
                            data: data

                        }]
                    });
            },
            error: function(data) {
               console.log("Ошибка при пострении графика!")
            }
        });

}



function drawPositionAvgSalaryChart(){

     $.ajax({
            type: 'GET',
            url: '/reports/get_position_salary_avg/',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                    console.log(data);
                $('#position_avg_salary').highcharts({
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: ''
                    },
                    subtitle: {

                    },
                    xAxis: {
                        type: 'category',
                        labels: {
                            rotation: -45,
                            style: {
                                fontSize: '13px',
                                fontFamily: 'Verdana, sans-serif'
                            }
                        }
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Зарплата (тыс.)'
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    tooltip: {

                    },
                    series: [{
                        name: 'Зарплата',
                        data: data,


                        dataLabels: {
                            enabled: true,
                            rotation: -90,
                            color: '#FFFFFF',
                            align: 'right',
                            format: '{point.y:.1f}', // one decimal
                            y: 10, // 10 pixels down from the top
                            style: {
                                fontSize: '13px',
                                fontFamily: 'Verdana, sans-serif'
                            }
                        }
                    }]
                });
            },
            error: function(data) {
               console.log("Ошибка при пострении графика!")
            }
        });

}
