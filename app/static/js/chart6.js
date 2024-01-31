$(document).ready(function() {
    const data = {
        labels: [
            'Mes 1',
            'Mes 2',
            'Mes 3'
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [156, 241, 208],
            backgroundColor: [
                'rgb(255, 99, 132, 0.6)',
                'rgb(54, 162, 235, 0.6)',
                'rgb(255, 205, 86, 0.6)'
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Consumo últimos 3 Meses',
                }
            },
        }
    };

    const ctx = document.getElementById('myChart6');

    const myChart = new Chart(ctx, config);
});