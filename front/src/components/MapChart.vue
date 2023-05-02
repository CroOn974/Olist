<template>
  <div id="container" style="height: 500px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name : 'MapChart',
  props:{
        option:{
            type: Object,
        }
    },
  watch: {
    option: {
      handler(newValue, oldValue) {
        console.log("old=",oldValue);
        console.log("new=",newValue);
        // Action à effectuer lorsque la valeur du prop change
        // Ici, on peut appeler une méthode pour mettre à jour la carte
        this.updateMapChart(newValue);
      },
      deep: true // permet de suivre les changements profonds dans l'objet
    }
  },
  methods: {
    updateMapChart(data){

      const chart = echarts.init(document.getElementById('container'));
    fetch('https://code.highcharts.com/mapdata/countries/br/br-all.geo.json')
      .then(response => response.json())
      .then(mapJson => {
        echarts.registerMap('brazil', mapJson);

        const name = mapJson.features.map(feature => {
          const postalCode = feature.properties['postal-code'];
          const name = feature.properties['name']
          return { name: name, code: postalCode };
        });

        const finalData = name.map(region => {
          const valueObj = data.find(v => v.code === region.code);
          return {
            name: region.name,
            value: valueObj ? valueObj.value : null
          };
        });

        // Trouver la valeur maximale
        const maxValue = Math.max(...data.map(item => item.value));

        // Trouver la valeur minimale
        const minValue = Math.min(...data.map(item => item.value));
        
        const option = {
          title: {
            text: 'Commandes par Régions',
            textStyle: {
              color: "#fff",
            },
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {c}'
          },
          visualMap: {
            min: minValue,
            max: maxValue,
            inRange: {
              color: ['#fff', '#007AFF']
            },
            text: ['High', 'Low'],
            calculable: true
          },
          series: [
            {
              type: 'map',
              map: 'brazil',
              label: {
                show: true
              },
              data: finalData,
            }
          ]
        };
        chart.setOption(option);
      });
    }
  }
};
</script>

<style>
#container {
  width: 100%;
  height: 100%;
}
</style>

