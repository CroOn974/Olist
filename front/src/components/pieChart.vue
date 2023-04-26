<template>
    <div class="">
        <v-chart class="chart w-auto " :option="option" autoresize=false />
    </div>
</template>
  
<script setup props="option">
    import { use } from 'echarts/core';
    import { CanvasRenderer } from 'echarts/renderers';
    import { PieChart } from 'echarts/charts';
    import {
        TitleComponent,
        TooltipComponent,
    } from 'echarts/components';
    import VChart, { THEME_KEY } from 'vue-echarts';
    import { provide } from 'vue';
    
    use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent]);
    
    provide(THEME_KEY, 'dark');
</script>

<script>
    export default {
        name:'PieChart',
        props:{
            option:{
                type: Object,
            }
        }
    }
</script>