<template>
  <Line :data="chartData" :options="chartOptions" />
</template>
  
<script>
  export default {
    name: 'MultiLineChart',
    components: { 
      
     },
    data() {
      return {
        chartData: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
          datasets: [
            {
              label: 'Data One',
              backgroundColor: '#FF5733',
              data: [40, 39, 10, 40, 39, 80, 40],
            },
            {
              label: 'Data Two',
              backgroundColor: '#0047AB',
              data: [4, 90, 15, 24, 80, 12, 40],
            },
            {
              label: 'Data Three',
              backgroundColor: '#00A36C',
              data: [20, 19, 40, 50, 30, 70, 45],
            },
          ],
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: true,
        }
      }
    }
  }
  </script>