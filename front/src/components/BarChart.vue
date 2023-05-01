<template>
    <div class="">
        <v-chart class="chart w-auto h-64" :option="option" autoresize />
    </div>
  </template>

<script setup props="option">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
    TitleComponent,
    TooltipComponent,
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { provide } from 'vue';

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent]);

provide(THEME_KEY, 'echarts');
</script>

  <script>
  
  export default {
    name: 'BarChart',
    props:{
        option:{
            type: Object,
        }
    },

    async created(){
        console.log("option =",this.option)
    },
  }
  </script>