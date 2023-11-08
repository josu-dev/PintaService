<script setup>
  import { APIService } from '@/utils/api';
  import { ref, watchEffect } from 'vue';

  /**
   * @typedef {{
   *  service:{
   *    id:string,
   *    name:string,
   *    enabled:boolean,
   *  },
   *  total_requests:number
   * }[]} APIResponse
   */

  /** @type {import('vue').Ref<APIResponse>} */
  const mostRequestedServices = ref([]);

  /** @type {import('vue').Ref<APIResponse>} */
  const tData = ref([]);

  APIService.get('/stats/most_requested_services', {
    onJSON(json) {
      mostRequestedServices.value = json.data;
    },
    onFailure(response) {
      console.log('Request failed');
    },
    onError(error) {
      console.log(error);
    }
  });

  watchEffect(() => {
    /** @type {APIResponse} */
    const data = [];
    if (!mostRequestedServices.value) {
      tData.value = data;
      return;
    }
    for (const item of mostRequestedServices.value) {
      data.push(item);
    }
    tData.value = data;
    console.log(data);
  });
</script>

<template>
  <div class="overflow-x-auto text-primary-content">
    <table class="table">
      <thead>
        <tr>
          <th class=""></th>
          <th class="">Nombre</th>
          <th class="">Habilitado</th>
          <th class="">Solicitudes</th>
        </tr>
      </thead>
      <tbody class="">
        <template v-for="(item, index) in tData" :key="item.id">
          <tr class="hover [&>td]:">
            <td>{{ index + 1 }}</td>
            <td>{{ item.service.name }}</td>
            <td>{{ item.service.enabled ? '✅' : '❌' }}</td>
            <td>{{ item.total_requests }}</td>
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
