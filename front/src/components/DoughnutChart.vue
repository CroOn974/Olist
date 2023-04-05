<template>
    <Doughnut
      id="doughnut-chart"
      :options="chartOptions"
      :data="chartData"
      :width="width"
      :height="height"
    />
  </template>
  
  <script>
  import { Doughnut } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

  ChartJS.register(ArcElement, Tooltip, Legend)

  export default {
    name: 'DoughnutChart',
    components: {
        Doughnut
    },
    props: {
      width: {
        type: Number,
        required: true
      },
      height: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        chartData: {
            labels: ['VueJs', 'EmberJs', 'ReactJs', 'AngularJs'],
            datasets: [
                {
                backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#DD1B16'],
                data: [40, 20, 80, 10]
                }
            ]
        },
        chartOptions: {
            responsive: true,
            maintainAspectRatio: false
        }
      }
    }
  }
  </script>