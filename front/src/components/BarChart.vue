<template>
    <Bar
      id="bar-chart"
      :options="chartOptions"
      :data="chartData"
    />
  </template>
  
  <script>
  
  export default {
    name: 'BarChart',
    components: { 
      
     },
    data() {
      return {
        chartData: {
          labels: [ 'January', 'February', 'March' ],
          datasets: [ { data: [40, 20, 12] } ]
        },
        chartOptions: {
            responsive: true,
            maintainAspectRatio: true,
        }
      }
    }
  }
  </script>