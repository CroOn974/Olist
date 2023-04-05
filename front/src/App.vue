<template>

  <div class="flex h-screen" id="dashboard">

    <div class="mr-8 h-screen w-1/4" id="colDough">
      <div>
        <DoughnutChart :width="300" :height="300"/>
      </div>
      <div class="my-8">
        <DoughnutChart :width="300" :height="300"/>
      </div>
    </div>

    <div class="w-3/4 m-auto grid grid-cols-2 gap-4" id="colBar">
      <div>
        <div><BarChart/></div>
        <div><BarChart :data="chartData"/></div>
      </div>
      <div>
        <div><MultiLineChart/></div>
        <div><MultiLineChart/></div>
        
      </div>
      
      
      
    </div>

  </div>
</template>

<script>
import BarChart from './components/BarChart.vue'
import DoughnutChart from './components/DoughnutChart.vue'
import MultiLineChart from './components/MultiLineChart.vue'

export default {
  name: 'App',
  components: { 
    BarChart,
    DoughnutChart,
    MultiLineChart
  },
  data(){
    return{
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
          ],
        },
    }
  }
}
</script>