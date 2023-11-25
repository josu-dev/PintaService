<script setup>
  import { APIService } from '@/utils/api';
  import { log } from '@/utils/logging';
  import {
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    Title,
    Tooltip
  } from 'chart.js';
  import { ref, watchEffect } from 'vue';
  import { Bar } from 'vue-chartjs';

  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

  /**
   * @typedef {{
   *  institution:{
   *    id:string,
   *    name:string,
   *    enabled:boolean,
   *  },
   *  avg_resolution_time:number
   * }[]} APIResponse
   *
   * @typedef {{
   *  labels: string[],
   *  datasets:{
   *    label:string,
   *    backgroundColor:string,
   *    data:number[],
   *  }[]
   * }} ChartData
   */

  /** @type {import('vue').Ref<APIResponse | undefined>} */
  const mostEfficientInstitutions = ref();
  /** @type {import('vue').Ref<ChartData | undefined>} */
  const chartData = ref();

  APIService.get('/stats/most_efficient_institutions', {
    onJSON(json) {
      mostEfficientInstitutions.value = json.data;
    },
    onFailure(response) {
      log.warn('stats', 'failed to get most efficient institutions', response);
    },
    onError(error) {
      log.error('stats', 'error getting most efficient institutions', error);
    }
  });

  watchEffect(() => {
    /** @type {ChartData} */
    const data = {
      labels: [],
      datasets: [
        {
          label: 'Tiempo de resolucion promedio',
          backgroundColor: '#03b675',
          data: []
        }
      ]
    };
    if (!mostEfficientInstitutions.value) {
      chartData.value = undefined;
      return;
    }
    for (const item of mostEfficientInstitutions.value) {
      data.labels.push(item.institution.name);
      data.datasets[0].data.push(item.avg_resolution_time);
    }
    chartData.value = data;
  });

  /** @type {any} */
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y'
  };
</script>

<template>
  <Bar
    v-if="chartData"
    id="stats-most-requested-services"
    :data="chartData"
    :options="chartOptions"
  />
</template>
