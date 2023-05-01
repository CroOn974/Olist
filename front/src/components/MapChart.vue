<template>
  <div id="container" style="height: 500px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name : 'MapChart',
  mounted() {
    const chart = echarts.init(document.getElementById('container'));
    fetch('https://code.highcharts.com/mapdata/countries/br/br-all.geo.json')
      .then(response => response.json())
      .then(mapJson => {
        echarts.registerMap('brazil', mapJson);
        const data = [
          { code: 'SP', value: 10 },
          { code: 'MA', value: 11 },
          { code: 'PA', value: 12 },
          { code: 'SC', value: 13 },
          { code: 'BA', value: 14 },
          { code: 'AP', value: 15 },
          { code: 'MS', value: 16 },
          { code: 'MG', value: 17 },
          { code: 'GO', value: 18 },
          { code: 'RS', value: 19 },
          { code: 'TO', value: 20 },
          { code: 'PI', value: 21 },
          { code: 'AL', value: 22 },
          { code: 'PB', value: 23 },
          { code: 'CE', value: 24 },
          { code: 'SE', value: 25 },
          { code: 'RR', value: 26 },
          { code: 'PE', value: 27 },
          { code: 'PR', value: 28 },
          { code: 'ES', value: 29 },
          { code: 'RJ', value: 30 },
          { code: 'RN', value: 31 },
          { code: 'AM', value: 32 },
          { code: 'MT', value: 33 },
          { code: 'DF', value: 34 },
          { code: 'AC', value: 35 },
          { code: 'RO', value: 36 }
        ];
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
            text: 'ECharts Maps basic demo',
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
};
</script>

<style>
#container {
  width: 100%;
  height: 100%;
}
</style>

