import { createApp } from 'vue'
import App from './App.vue'
import Chart from 'chart.js'
import './assets/tailwind.css'

createApp(App).use(Chart).mount('#app')
