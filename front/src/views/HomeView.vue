<template>
  <!-- MAIN CONTAINER  -->
  <div class="container bg-slate-900 h-screen overflow-y-hidden">

    <NavBar/>

    <!-- DASHBOARD CONTAINER -->
    <div class="flex flex-nowrap overflow-x-scroll min-w-full overflow-y-hidden" id="dashboard">

      <!-- COLONNE 1 -->
      <div class="w-1/4 h-full flex-shrink-0" id="colDough">
        <!-- SELECT ANNEE -->
        <select class=" h-8 m-4 px-2 rounded-xl" v-model="selectedYear" @change="updateDash()">
          <option v-for="year in years" :value="year" :key="year">{{ year }}</option>
        </select>
        <DoughnutChart class="" :option="option_pie_1"/>
        <DoughnutChart :option="option_pie_2"/>
      </div>

      <!-- COLONNE 2 -->
      <div class="w-1/2 flex-shrink-0 bg-slate-800">
        <div class="h-64 pt-8 border-b-2 border-b-slate-500">
          <BarChart :option="option_multibar_1"/>
        </div>
        <div class="h-48 my-4 border-b-2 border-b-slate-500">
          <MultiLineChart class="" :option="option_multiline_1"/>
        </div>
        <div class="h-48 mt-4">
          <MultiLineChart class="" :option="option_multiline_1"/>
        </div>
      </div>

      <!-- COLONNE 3 -->
      <div class="w-1/4 mx-4 flex-shrink-0">
        <!-- Panier Moyen & marge + coûts -->
        <div class="h-48 mt-8 mx-4 rounded-lg shadow-lg border-2 border-slate-500 ">
          <div class="grid grid-cols-2 h-full">
            <div class="rounded-lg p-4">
              <p class="text-gray-50 font-medium mb-8">Panier Moyen</p>
              <p class="text-gray-50 text-5xl text-center">{{turnover[0].avg_basket}}€</p>
            </div>
            <div class="grid grid-rows-2">
              <div class="p-2 border-b-4 border-b-blue-500 border-l-4 border-l-green-400">
                <p class="text-gray-50 mb-2 font-medium">Bénéfices</p>
                <p class="text-gray-50 text-3xl text-center">{{(turnover[0].avg_basket * 3)/100}}€</p>
              </div>
              <div class="p-2 border-l-4 border-orange-500">
                <p class="text-gray-50 mb-2 font-medium">Coûts</p>
                <p class="text-gray-50 text-3xl text-center">{{turnover[0].avg_basket - (turnover[0].avg_basket * 3)/100}} €</p>
              </div>
            </div>
          </div>
        </div>
        <!-- Nombre nouveau clients & nouveaux rebonds -->
        <div class="h-48 my-8">
          <div class="grid grid-cols-2">
            <div class="mx-4 rounded-lg shadow-lg border-2 border-green-300 h-48 p-4">
              <p class="text-gray-50">Nouveaux Clients</p>
              <p class="text-gray-50 text-5xl text-center mt-8">{{newCustomers.new_customers_count}}</p>
            </div>
            <div class="mx-4 rounded-lg shadow-lg border-2 border-blue-500 h-48 pt-4">
              <p class="text-gray-50 text-center">Rebonds</p>
              <p class="text-gray-50 text-5xl text-center mt-6">{{newTurnovers}}</p>
            </div>
          </div>
        </div>
        <BarChart :option="option_bar_2"/>
      </div>

      <!-- COLONNE 4 -->
      <div class="w-1/4 h-min my-auto flex-shrink-0">
        <div class=" h-min"> 
          <MapChart class="" :option="mapData"/>
        </div>
        
      </div>
    
    </div>
  </div>
</template>

<script>
// import NavBar from '../components/NavBar.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import BarChart from '../components/BarChart.vue'
import MultiLineChart from '../components/MultiLineChart.vue'
import MapChart from '@/components/MapChart.vue'

export default {
  name: 'HomeView',
  components: { 
    DoughnutChart,
    MultiLineChart,
    BarChart,
    // NavBar,
    MapChart
  },
  data(){
    return{
      selectedYear: '2017',
      years: ['201','2017', '2018', '2019'],
      limit: '5',
      listState : [],
      listProduct : [],
      option_bar_1 : {
        title: {
          text: 'Top 5 Produits',
          left: 'center',
          top:'5%',
          textStyle: {
            color: "#fff",
          },
        },
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          axisLabel:{
            color:'#FFF'
          }
        },
        yAxis: {
          show: false
        },
        series: [
          {
            data: [120, 200, 150, 80, 70, 110, 130],
            type: 'bar',
            itemStyle: {
              borderRadius: [30, 30, 0, 0]
            },
            label: {
              show: true,
              position: "top",
              distance: 15,
              color: "#fff",
              fontSize: 10,
            }
          }
        ]
      },
      option_bar_2 : {
        title: {
          text: 'local VS inter',
          left: 'center',
          top:'2%',
          textStyle: {
            color: "#fff",
          },
        },
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
          axisLabel:{
            color:'#FFF'
          }
        },
        yAxis: {
          show: false
        },
        series: [
          {
            data: [120, 200, 150, 80, 70],
            type: 'bar',
            itemStyle: {
              borderRadius: [30, 30, 0, 0]
            },
            label: {
              show: true,
              position: "top",
              distance: 15,
              color: "#fff",
              fontSize: 10,
            }
          },
          {
            data: [99, 53, 128, 87, 192],
            type: 'bar',
            itemStyle: {
              borderRadius: [30, 30, 0, 0]
            },
            label: {
              show: true,
              position: "top",
              distance: 15,
              color: "#fff",
              fontSize: 10,
            }
          }
        ]
      },
      option_pie_1: {
        title: {
          text: 'Top 5 Produits',
          left: 'center',
          textStyle: {
            color: "#fff",
          },
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
            label: {
              color: '#fff'
            },
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
          textStyle: {
            color: "#fff",
          },
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
            label: {
              color: '#fff'
            },
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
      option_multibar_1 : {
            title: {
              text: 'Top 5 Produits',
              left: '2%',
              top:'2%',
              textStyle: {
                color: "#fff",
              },
            },
            legend: {
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
              left: '0%',
              top:'center',
              orient: 'vertical'
            },
            xAxis: {
              type: 'category',
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
              axisLabel:{
                  color:'#FFF'
                }
            },
            yAxis: {
              show: false
            },
            grid: {
              containLabel: true
            },
            series: [
            {
              type: 'bar',
              data: [44, 46, 49, 52, 55],
              barWidth: 15,
              itemStyle: {
                barBorderRadius: [30, 30, 0, 0]
              },
              label: {
                show: true,
                position: "top",
                distance: 15,
                color: "#fff",
                fontSize: 10,
              }
            },
            {
              type: 'bar',
              data: [58, 62, 65, 61, 59],
              barWidth: 15,
              itemStyle: {
                barBorderRadius: [30, 30, 0, 0]
              },
              label: {
                show: true,
                position: "top",
                distance: 15,
                color: "#fff",
                fontSize: 10,
              }
            },
            {
              type: 'bar',
              data: [33, 27, 29, 35, 39],
              barWidth: 15,
              itemStyle: {
                barBorderRadius: [30, 30, 0, 0]
              },
              label: {
                show: true,
                position: "top",
                distance: 15,
                color: "#fff",
                fontSize: 10,
              }
            },
            {
              type: 'bar',
              data: [16, 19, 14, 20, 22],
              barWidth: 15,
              itemStyle: {
                borderRadius: [30, 30, 0, 0]
              },
              label: {
                show: true,
                position: "top",
                distance: 15,
                color: "#fff",
                fontSize: 10,
              }
            },
            {
              type: 'bar',
              data: [65, 78, 81, 90, 54],
              barWidth: 15,
              itemStyle: {
                barBorderRadius: [30, 30, 0, 0]
              },
              label: {
                show: true,
                position: "top",
                distance: 15,
                color: "#fff",
                fontSize: 10,
              }
            }
          ]
      },
      option_multiline_1 : {
        title: {
          text: 'Stacked Line',
          left: '2%',
          top:'5%',
          textStyle: {
            color: "#fff",
          },
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine'],
          right: '0%',
          top:'center',
          orient: 'vertical',
          textStyle: {
            color: "#fff",
          },
        },
        grid: {
          left: '5%',
          right: '20%',
          bottom: '15%',
          containLabel: true
        },

        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          axisLabel:{
            color:'#FFF'
          }
        },
        yAxis: {
          show: false
        },
        series: [
          {
            name: 'Email',
            type: 'line',
            stack: 'Total',
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: 'Union Ads',
            type: 'line',
            stack: 'Total',
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: 'Video Ads',
            type: 'line',
            stack: 'Total',
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: 'Direct',
            type: 'line',
            stack: 'Total',
            data: [320, 332, 301, 334, 390, 330, 320]
          },
          {
            name: 'Search Engine',
            type: 'line',
            stack: 'Total',
            data: [820, 932, 901, 934, 1290, 1330, 1320]
          }
        ]
      },
      dataState:[],
      dataProduct:[],
      newCustomers:0,
      turnover:[
        {
        "year": "",
        "turnover": 0,
        "turnover_percentage": 0,
        "avg_basket": 0
      }
    ],
    mapData:[],
    }
  }
  ,
  /**
   * Récupère des données
   * 
   * 
   */
  async created(){
    this.updateDash()
  },
  methods: {
    updateDash(){
      this.topState(this.selectedYear, this.limit)
      this.topProduct(this.selectedYear, this.limit)
      this.get_new_customers(this.selectedYear)
      this.get_turnover(this.selectedYear)
      this.get_map_data(this.selectedYear,9)
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

    async get_new_customers(year){
      var response = await fetch('http://localhost:8000/api/customers-year/'+year+'/');
      let data = await response.json();
      console.log(data)
      this.newCustomers = data
    },
    async get_turnover(year){
      var response = await fetch('http://localhost:8000/api/turnover-year/'+year+'/');
      let data = await response.json();
      console.log(data)
      this.turnover = data
    },
    async get_map_data(year,limit){
      var response = await fetch('http://localhost:8000/api/state-year/'+year+'/'+limit+'');
      let data = await response.json();
      console.log(data)
      this.mapData = []
      data.forEach(d => {
        let i = {code:'', value:''}
        i.code = d.state_name
        i.value = d.quantity
        this.mapData.push(i)
      });
    },

  }
}
</script>
