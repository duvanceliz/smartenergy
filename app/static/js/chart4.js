$(document).ready(function() {

    const labels = [0, 0, 0, 0, 0];

    const data = {
        labels: labels,
        datasets: [{
            label: 'Curva 1',
            backgroundColor: "rgb(132,186,91,0.2)",
            borderColor: "rgb(204, 37, 41)",
            data: [0, 10, 5, 2, 20],
            tension: 0.1
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Factor de Potencia en Tiempo Real',
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Fecha'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '%'
                    },
                    min: 0,
                    max: 100,
                }
            }

        }
    };

    const ctx = document.getElementById('myChart4')

    const myChart = new Chart(ctx, config);

    const source = new EventSource("/datos_monitoreo");

    source.onmessage = function(event) {

        const data = JSON.parse(event.data);

        document.getElementById('value4').innerHTML = Math.round(data.dato);

        if (config.data.labels.length == 5) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }

        config.data.labels.push(data.fecha);
        config.data.datasets[0].data.push(data.dato);
        myChart.update();
    }
});