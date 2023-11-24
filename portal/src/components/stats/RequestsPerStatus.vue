<script setup>
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { requestStatus } from '@/utils/enums';
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
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const userStore = useUserStore();
  const toastStore = useToastStore();

  function submitLogout() {
    userStore.clearUser();
    router.push({
      name: 'login'
    });
  }

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
      if (response.status === 401) {
        submitLogout();
        toastStore.error('Expiro la sesion');
      }
      requestsPerStatus.value = [];
      console.warn(response);
    },
    onError(error) {
      requestsPerStatus.value = [];
      console.error(error);
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
