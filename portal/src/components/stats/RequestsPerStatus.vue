<script setup>
  import {
    ArcElement,
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    Title,
    Tooltip
  } from 'chart.js'
  import { Pie } from 'vue-chartjs'

  import { ref, watchEffect } from 'vue'
  import { APIService } from '../../utils/api'
  import { RequestStatus } from '../../utils/enums'
  ChartJS.register(Title, Tooltip, ArcElement, Legend, BarElement, CategoryScale, LinearScale)

  const requestsPerStatus = ref(null)

  APIService.get('/stats/requests_per_status')
    .then((response) => {
      requestsPerStatus.value = response.data
      console.log(response)
    })
    .catch((error) => {
      requestsPerStatus.value = null
      console.log(error)
    })

  const chartData = ref(null)

  const statusColors = {
    [RequestStatus.ACCEPTED]: '#3abff8',
    [RequestStatus.REJECTED]: '#f87272',
    [RequestStatus.IN_PROCESS]: '#f89123',
    [RequestStatus.CANCELED]: '#a6adba',
    [RequestStatus.FINISHED]: '#36d399'
  }

  watchEffect(() => {
    const data = { labels: [], datasets: [{ data: [], backgroundColor: [] }] }
    if (!requestsPerStatus.value) {
      chartData.value = data
      return
    }
    for (const status of requestsPerStatus.value) {
      data.labels.push(status.status)
      data.datasets[0].backgroundColor.push(statusColors[status.status])
      data.datasets[0].data.push(status.count)
    }
    chartData.value = data
    console.log(data)
  })

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
  }
</script>

<template>
  <Pie id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>
