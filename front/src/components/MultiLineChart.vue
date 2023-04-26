<template>
  <div class="">
      <v-chart class="chart h-80 bg-slate-50" :option="option" :autoresize=false />
  </div>
</template>

<script setup props="option">
  import { use } from 'echarts/core';
  import { CanvasRenderer } from 'echarts/renderers';
  import { LineChart } from 'echarts/charts';
  import { TitleComponent, GridComponent, TooltipComponent, ToolboxComponent } from 'echarts/components';
  import VChart, { THEME_KEY } from 'vue-echarts';
  import { provide } from 'vue';
  
  use([ CanvasRenderer, LineChart, TitleComponent, TooltipComponent, GridComponent, ToolboxComponent ]);
  
  provide(THEME_KEY, 'dark');
</script>

<script>
  export default {
      name:'multiLineChart',
      props:{
          option:{
              type: Object,
          }
      }
  }
</script>