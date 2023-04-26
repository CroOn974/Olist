<template>
<div class="container overflow-hidden">
  <NavBar/>
  <div class="flex h-screen ">
    <div class="w-1/4 h-full my-auto">
      <PieChart class="h-1/2 pb-2" :option="option_pie_1"/>
      <PieChart class="h-1/2 pt-2" :option="option_pie_2"/>
    </div>

    <div class="w-1/4 my-auto mx-4 space-y-4">
      <MapChart/>
    </div>
    <div class="w-1/2 h-full my-6 overflow-y-auto space-y-4 pr-2">
      <multiLineChart class="" :option="option_multiline_1"/>
      <BarChart class="" :option="option_multibar_1"/>
      <multiLineChart class="" :option="option_multiline_1"/>
      <BarChart class="" :option="option_bar_1"/>
      <BarChart class="" :option="option_bar_2"/>
      
    </div>
    
  </div>
</div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import BarChart from '../components/BarChart.vue'
import PieChart from '../components/pieChart.vue'
import multiLineChart from '../components/multiLineChart.vue'
import MapChart from '@/components/MapChart.vue'

export default {
  name: 'HomeView',
  components: { 
    BarChart,
    PieChart,
    multiLineChart,
    NavBar,
    MapChart
  },
  data(){
    return {
      option_pie_1: {
        title: {
          text: 'Top 5 Régions',
          left: 'center',
          top: '10%'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: [ '20%', '40%'],
            label:{
              color: "#fff",
            },
            emphasis: {
              label: {
                fontWeight: 'bold'
              }
            },

            data: [
              { value: 1048, name: 'Search Engine' },
              { value: 735, name: 'Direct' },
              { value: 580, name: 'Email' },
              { value: 484, name: 'Union Ads' },
              { value: 300, name: 'Video Ads' }
            ]
          }
        ]
      },
      option_pie_2: {
        title: {
          text: 'Top 5 Régions',
          textColor: "#fff",
          left: 'center',
          top: '10%'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        series: [
          {
            name: 'Traffic Sources',
            type: 'pie',
            radius: ['20%','40%'],
            center: ['50%', '50%'],
            label:{
              color: "#fff",
            },
            data: [
              { value: 335, name: 'Direct' },
              { value: 310, name: 'Email' },
              { value: 234, name: 'Ad Networks' },
              { value: 135, name: 'Video Ads' },
              { value: 1548, name: 'Search Engines' },
            ],
            emphasis: {
              label: {
                fontWeight: 'bold'
              }
            },
          },
        ],
      },
      option_bar_1 : {
        title: {
          text: 'Top 5 Produits',
          left: 'center',
          top:'5%'
        },
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
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
          top:'2%'
        },
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
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
      option_multibar_1 : {
        title: {
          text: 'Top 5 Produits',
          left: 'center',
          top:'5%'
        },
        legend: {
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
          left: '0%',
          top:'center',
          orient: 'vertical'
        },
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
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
          left: 'center',
          top:'5%'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine'],
          right: '0%',
          top:'center',
          orient: 'vertical'
        },
        grid: {
          left: '5%',
          right: '20%',
          bottom: '15%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value'
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
      }
    }
  }
}
</script>
