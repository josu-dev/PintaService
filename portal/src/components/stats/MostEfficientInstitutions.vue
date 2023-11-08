<script setup>
  import { ref, watchEffect } from 'vue'
  import { APIService } from '../../utils/api'

  const mostEfficientInstitutions = ref(null)
  const tData = ref(null)

  APIService.get('/stats/most_efficient_institutions')
    .then((response) => {
      mostEfficientInstitutions.value = response.data
      console.log(response)
    })
    .catch((error) => {
      mostEfficientInstitutions.value = null
      console.log(error)
    })

  watchEffect(() => {
    const data = []
    if (!mostEfficientInstitutions.value) {
      tData.value = data
      return
    }
    for (const item of mostEfficientInstitutions.value) {
      data.push(item)
    }
    tData.value = data
    console.log(data)
  })
</script>

<template>
  <div class="overflow-x-auto text-primary-content">
    <table class="table">
      <thead>
        <tr>
          <th class=""></th>
          <th class="">Nombre</th>
          <th class="">Habilitada</th>
          <th class="">Tiempo de resolucion promedio</th>
        </tr>
      </thead>
      <tbody class="">
        <template v-for="(item, index) in tData" :key="item.id">
          <tr class="hover [&>td]:">
            <td>{{ index + 1 }}</td>
            <td>{{ item.institution.name }}</td>
            <td>{{ item.institution.enabled ? '✅' : '❌' }}</td>
            <td>{{ item.avg_resolution_time }}</td>
          </tr>
        </template>
        <template v-if="tData.length === 0">
          <tr>
            <td colspan="4" class="text-center">No hay servicios</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
