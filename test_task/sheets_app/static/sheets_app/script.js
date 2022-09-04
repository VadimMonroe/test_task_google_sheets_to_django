// ------------- google charts version (for browsers, which canvas don't working) -------------

// const id = document.querySelectorAll('#id');
// const order_number = document.querySelectorAll('#order_number');
// const cost = document.querySelectorAll('#cost');
// const deliveryTime = document.querySelectorAll('#delivery_time');
// const icostRoubles = document.querySelectorAll('#cost_roubles');

// let list_data = [];
// let labels = [];

// let listCostDate = [['Cost', 'Date'],];

// for (let i = 0; i < id.length; i++) {
//     list_data.push(Number(cost[i].textContent));
//     labels.push(deliveryTime[i].textContent);
//     listCostDate.push([deliveryTime[i].textContent, Number(cost[i].textContent)])
// }

// function drawChart() {
//     const data = google.visualization.arrayToDataTable(listCostDate.slice(0, 26));

//     const options = {
//         chart: {
//             title: 'Roubles',
//             subtitle: 'From USD',
//             curveType: 'none'},
//         width: 900,
//         height: 500,
//         bar: {groupWidth: '95%'},
//         vAxis: { 
//             gridlines: { count: 15 }}
//     };

//     const chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
//     chart.draw(data, options);
// }

// google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(drawChart);


// ------------- canvas version -------------

const deliveryTime = document.querySelectorAll('#delivery_time');
const costRoubles = document.querySelectorAll('#cost_roubles');
const totalPrice = document.querySelector('.totalPriceH1');

let list_cost = [];
let list_date = [];
let totalPriceRoubles = 0;

for (let i = 0; i < id.length; i++) {
    roubles = Number(costRoubles[i].textContent);

    list_cost.push(roubles);
    list_date.push(deliveryTime[i].textContent);

    totalPriceRoubles += roubles;
}

totalPrice.textContent = totalPriceRoubles;

const data = {
    labels: list_date,
    datasets: [{
      label: 'Roubles',
      backgroundColor: 'white',
      borderColor: '#3366CC',
      data: list_cost,
    }]
};

const ctx = document.getElementById('myChart').getContext('2d');

// ctx.canvas.parentNode.style.width= '600px';
// ctx.canvas.parentNode.style.height = '300px';

const myChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        maintainAspectRatio: true,
        parsing: {
            xAxisKey: 'data\\.key',
            yAxisKey: 'data\\.value'
        },
        elements: {
            line: {
                tension: 0.2
            }
        },
        datasets: {
            line: {
                pointRadius: 2
            }
        },
        scales: {
            x: {
                max: 50
              },
            y: {
                stacked: true
            },
        }
    }
});
