<script setup>
  import { APIService } from '@/utils/api';
  import { ref, watchEffect } from 'vue';

  /**
   * @typedef {{
   *  institution:{
   *    id:string,
   *    name:string,
   *    enabled:boolean,
   *  },
   *  avg_resolution_time:number
   * }[]} APIResponse
   */

  /** @type {import('vue').Ref<APIResponse>} */
  const mostEfficientInstitutions = ref([]);

  /** @type {import('vue').Ref<APIResponse>} */
  const tData = ref([]);

  APIService.get('/stats/most_efficient_institutions', {
    onJSON(json) {
      mostEfficientInstitutions.value = json.data;
    },
    onFailure(response) {
      console.warn('Request failed');
    },
    onError(error) {
      console.error(error);
    }
  });

  watchEffect(() => {
    /** @type {APIResponse} */
    const data = [];
    if (!mostEfficientInstitutions.value) {
      tData.value = data;
      return;
    }
    for (const item of mostEfficientInstitutions.value) {
      data.push(item);
    }
    tData.value = data;
    console.log(data);
  });
</script>

<template>
  <div class="overflow-x-auto text-primary-content rounded-3xl shadow">
    <table class="table w-full">
      <thead>
        <tr>
          <th class=""></th>
          <th class="">Nombre</th>
          <th class="">Tiempo de resolucion promedio</th>
          <th class="">Habilitada</th>
        </tr>
      </thead>
      <tbody class="">
        <template v-for="(item, index) in tData" :key="item.id">
          <tr class="hover text-center">
            <td>{{ index + 1 }}</td>
            <td>{{ item.institution.name }}</td>
            <td>{{ item.avg_resolution_time }}</td>
            <td>{{ item.institution.enabled ? '✅' : '❌' }}</td>
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
