<script setup>
  import { APIService } from '@/utils/api';
  import { requestStatus } from '@/utils/enums';
  import { log } from '@/utils/logging';
  import {
    ArcElement,
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    Title,
    Tooltip
  } from 'chart.js';
  import { ref, watchEffect } from 'vue';
  import { Pie } from 'vue-chartjs';

  ChartJS.register(Title, Tooltip, ArcElement, Legend, BarElement, CategoryScale, LinearScale);

  /**
   * @typedef {{
   *  status: import('@/utils/enums').RequestStatus,
   *  count:number
   * }[]} APIResponse
   *
   * @typedef {{
   *  labels: (import('@/utils/enums').RequestStatus)[],
   *  datasets:{
   *    data:any[],
   *    backgroundColor:string[]
   *  }[]
   * }} ChartData
   */

  /** @type {import('vue').Ref<APIResponse>} */
  const requestsPerStatus = ref([]);

  APIService.get('/stats/requests_per_status', {
    onJSON(json) {
      requestsPerStatus.value = json.data;
    },
    onFailure(response) {
      log.warn('stats', 'failed to get requests per status', response);
      requestsPerStatus.value = [];
    },
    onError(error) {
      log.error('stats', 'error getting requests per status', error);
      requestsPerStatus.value = [];
    }
  });

  /** @type {import('vue').Ref<ChartData>} */
  const chartData = ref(/** @type {any} */ (null));

  const statusColors = {
    [requestStatus.ACCEPTED]: '#3abff8',
    [requestStatus.REJECTED]: '#f87272',
    [requestStatus.IN_PROCESS]: '#f89123',
    [requestStatus.CANCELED]: '#a6adba',
    [requestStatus.FINISHED]: '#36d399'
  };

  watchEffect(() => {
    /** @type {ChartData} */
    const data = { labels: [], datasets: [{ data: [], backgroundColor: [] }] };
    if (!requestsPerStatus.value) {
      chartData.value = data;
      return;
    }
    for (const status of requestsPerStatus.value) {
      data.labels.push(status.status);
      data.datasets[0].backgroundColor.push(statusColors[status.status]);
      data.datasets[0].data.push(status.count);
    }
    chartData.value = data;
  });

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
  };
</script>

<template>
  <Pie id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>
