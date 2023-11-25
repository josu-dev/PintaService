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
   *  service:{
   *    id:string,
   *    name:string,
   *    enabled:boolean,
   *  },
   *  total_requests:number
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
  const mostRequestedServices = ref();
  /** @type {import('vue').Ref<ChartData | undefined>} */
  const chartData = ref();

  APIService.get('/stats/most_requested_services', {
    onJSON(json) {
      mostRequestedServices.value = json.data;
    },
    onFailure(response) {
      log.warn('stats', 'failed to get most requested services', response);
    },
    onError(error) {
      log.error('stats', 'error getting most requested services', error);
    }
  });

  watchEffect(() => {
    /** @type {ChartData} */
    const data = {
      labels: [],
      datasets: [
        {
          label: 'Cantidad de solicitudes',
          backgroundColor: '#1279ff',
          data: []
        }
      ]
    };
    if (!mostRequestedServices.value) {
      chartData.value = undefined;
      return;
    }
    for (const item of mostRequestedServices.value) {
      data.labels.push(item.service.name);
      data.datasets[0].data.push(item.total_requests);
    }
    chartData.value = data;
  });

  /** @type {any} */
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
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
