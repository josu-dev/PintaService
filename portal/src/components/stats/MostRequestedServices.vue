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
      console.warn('Request failed');
    },
    onError(error) {
      console.error(error);
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
  });
</script>

<template>
  <div class="overflow-x-auto text-primary-content rounded-3xl shadow">
    <table class="table w-full">
      <thead>
        <tr>
          <th class=""></th>
          <th class="">Nombre</th>
          <th class="w-full p-0"></th>
          <th class="">Solicitudes</th>
          <th class="">Habilitado</th>
        </tr>
      </thead>
      <tbody class="">
        <template v-for="(item, index) in tData" :key="item.id">
          <tr class="hover">
            <td>{{ index + 1 }}</td>
            <td colspan="2">{{ item.service.name }}</td>
            <td class="text-center">{{ item.total_requests }}</td>
            <td class="text-center">{{ item.service.enabled ? '  ✅' : '❌' }}</td>
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
