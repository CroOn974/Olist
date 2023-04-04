<template>
  <VuePlotly :data="data" :layout="layout" :display-mode-bar="false"></VuePlotly>
</template>

<script>
import { VuePlotly } from 'vue3-plotly'

export default {
  name:'App',
  components: {
    VuePlotly
  },
  data() {
    return {
      data:[{
        x: [1,2,3,4],
        y: [10,15,13,17],
        type:"bar"
      }],
      layout:{
        title: "My graph"
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
