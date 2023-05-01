<template>
  <div ref="chart" style="width: 100%; height: 500px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  props: ['option'],
  mounted() {
    // création du graphique avec l'option passée en tant que propriété
    const chart = echarts.init(this.$refs.chart);
    chart.setOption(this.option);
  },
};
</script>