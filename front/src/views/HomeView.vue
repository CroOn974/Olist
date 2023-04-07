<template>
<div class="container h-screen">
  <NavBar/>
  <div class="flex bg-slate-100 " id="dashboard">
    <div class="mr-8 w-1/3 h-auto" id="colDough">
      <div class="">
        <DoughnutChart :option="option_pie_1"/>
      </div>
      <div >
        <DoughnutChart :option="option_pie_2"/>
      </div>
    </div>

    <div class="w-3/4 grid grid-cols-2 gap-4" id="colBar">
      <div class="col">
        <div class="row">
            <h3>BarChart CA</h3>
            <BarChart/>
        </div>
        
        <div class="row">
          <h3>BarChart Local vs Inter</h3>
          <BarChart :data="chartData"/>
        </div>
      </div>

      <div class="col">
        <div class="row">
          <h3>Top 5 Produits</h3>
          <MultiLineChart/>
        </div>
        <div class="row">
          <h3>Top 5 Régions</h3>
          <MultiLineChart/>
        </div>
        
      </div>
      
    </div>

  </div>
</div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import BarChart from '../components/BarChart.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import MultiLineChart from '../components/MultiLineChart.vue'

export default {
  name: 'HomeView',
  components: { 
    BarChart,
    DoughnutChart,
    MultiLineChart,
    NavBar
  },
  data(){
    return{
      option_pie_1: {
        title: {
          text: 'Top 5 Produits',
          left: 'center',
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        series: [
          {
            name: 'Nombre de ventes',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            data: [
              { value: 335, name: 'Direct' },
              { value: 310, name: 'Email' },
              { value: 234, name: 'Ad Networks' },
              { value: 135, name: 'Video Ads' },
              { value: 1548, name: 'Search Engines' },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      },
      option_pie_2: {
        title: {
          text: 'Top 5 Régions',
          left: 'center',
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        series: [
          {
            name: 'CA',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            data: [
              { value: 335, name: 'Direct' },
              { value: 310, name: 'Email' },
              { value: 234, name: 'Ad Networks' },
              { value: 135, name: 'Video Ads' },
              { value: 1548, name: 'Search Engines' },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      },
      
    }
  }
}
</script>
