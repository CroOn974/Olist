<template>
<div class="container h-screen">
  <NavBar/>
  <div class="flex bg-slate-100 " id="dashboard">
    <select v-model="selectedYear" @change="updateDash()">
      <option v-for="year in years" :value="year" :key="year">{{ year }}</option>
    </select>
    <div class="mr-8 w-1/3 h-auto" id="colDough">
      <div class="">
        <DoughnutChart :option="option_pie_1"/>
      </div>
      <div >
        <DoughnutChart :option="option_pie_2"/>
      </div>
    </div>

    <div class="w-3/4 grid grid-cols-2 gap-4" id="colBar">
      <BarChart :option="barChartOptions" />
    </div>

  </div>
</div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import BarChart from '../components/BarChart.vue'

export default {
  name: 'HomeView',
  components: { 
    DoughnutChart,
    NavBar,
    BarChart
  },
  data(){
    return{
      selectedYear: '',
      years: ['2017', '2018', '2019'],
      limit: '5',
      listState : [],
      listProduct : [],
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
            data: [],
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
      dataState:[],
      dataProduct:[],
      barChartOptions: {
        // les options du graphique
        title: {
          text: 'Mon graphique à barres'
        },
        xAxis: {
          data: []
        },
        yAxis: {},
        series: []
      }
    }
  }
  ,
  /**
   * Récupère des données
   * 
   * 
   */
  async created(){
    
  },
  methods: {
    updateDash(){
      this.topState(this.selectedYear, this.limit)
      this.topProduct(this.selectedYear, this.limit)
    },
    async topState(year, limit){
      
      var response = await fetch('http://localhost:8000/api/state-year/'+year+'/'+limit+'');
      let data = await response.json();

      this.option_pie_2.series[0].data = data.map((item) => {
        return { value: item.turnover, name: item.state_name };
      });

      this.listState = data.map((item) => item.state_name);
      this.evoState()

    },
    async topProduct(year, limit){

      var response = await fetch('http://localhost:8000/api/product-year/'+year+'/'+limit+'');
      let data = await response.json();
      
      this.option_pie_1.series[0].data = data.map((item) => {
        return { value: item.turnover, name: item.product_id };
      });

      this.listProduct = data.map((item) => item.product_id);
      this.evoProduct()
    },
    async evoState(){
      const states = this.listState.join(',');
      var response = await fetch('http://localhost:8000/api/states-evo/'+states+'/');
      let data = await response.json();
      console.log(data)
      this.dataState = data
      

    },    
    async evoProduct(){
      const product = this.listProduct.join(',');
      var response = await fetch('http://localhost:8000/api/product-evo/'+product+'/');
      let data = await response.json();
      console.log(data)
      this.dataProduct = data
    },

  }
}
</script>
