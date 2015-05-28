$(function () {

    var currentYear = new Date().getFullYear();

    drawVacanciesDistributionChart();
    drawPositionAvgSalaryChart();

    var hiredToTotalChart = drawHiredToTotalApplicantsRate(HiredToTotalApplicantsGetData(currentYear));

    $("#slct_change_year").on("change",function(){
               var selected_year = $(this).val();
               data = HiredToTotalApplicantsGetData(selected_year)
               hiredToTotalChart.series[0].setData(data['total'])
               hiredToTotalChart.series[1].setData(data['hired'])

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
                            text: 'Распределение вакансий по должностям'
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
                        text: 'Средняя запрашиваемая зарплата'
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





function HiredToTotalApplicantsGetData(year){
     var chart_data;
     $.ajax({
            type: 'GET',
            url: '/reports/hired_to_total_rate',
            dataType: 'json',
            contentType: 'application/json',
            async: false,
            data:{
                'year':year
            },
            success: function (data) {
                    console.log(data);
                    chart_data = data;


            },
            error: function(data) {

            }
        });

     console.log("dsds"+chart_data);
     return chart_data;
}

function drawHiredToTotalApplicantsRate(data){


    var chart = $('#hired_to_total_rate').highcharts({
                        chart: {
                            type: 'line'
                        },
                        title: {
                            text: 'Monthly Average Temperature'
                        },
                        subtitle: {
                            text: 'Source: WorldClimate.com'
                        },
                        xAxis: {
                            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        },
                        yAxis: {
                            title: {
                                text: 'Temperature (°C)'
                            }
                        },
                        plotOptions: {
                            line: {
                                dataLabels: {
                                    enabled: true
                                },
                                enableMouseTracking: false
                            }
                        },
                        series: [{
                            name: 'Всего кандидатов',
                            data: data['total']
                        }, {
                            name: 'Принятно на работу',
                            data:  data['hired']
                        }]
                    });


    return chart;

}