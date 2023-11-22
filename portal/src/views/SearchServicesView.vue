<script setup>
import { APIService } from '@/utils/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
/**
 * @typedef {{
 *    id: string,
 *    name: string,
 *    description: string,
 *    laboratory: string,
 *    keywords: string[],
 *    enabled: boolean,
 *    service_type: string,
 * }} ServiceData[]
 */
/** @type {import('vue').Ref<ServiceData[]>} */
const servicesList = ref([]);
const qFilter = ref('');
const typeFilter = ref('todos');
const router = useRouter();
const loading = ref(false);

let currentPage = ref(1);
let perPage = ref(0);
let totalServices = ref(0);

const filterServices = () => {
  loading.value = true;
  console.log('CurrentPage', currentPage.value)
  const url = `/services/search?q=${qFilter.value}&type=${typeFilter.value}&page=${currentPage.value}`;
  APIService.get(url, {
    onJSON(json) {
      servicesList.value = json.data;
      currentPage.value = json.page;
      perPage.value = json.per_page;
      totalServices.value = json.total;
      loading.value = false;
    },
    onFailure(response) {
      console.log('Request failed');
    },
    onError(error) {
      console.log(error);
    }
  });
};
filterServices();
const redirectToDetail = (serviceId) => {
  if (!serviceId) return;
  router.push(`/services/${serviceId}`);
};

const changePage = (page) => {
  if (page >= 1 && page <= Math.ceil(totalServices.value / perPage.value)) {
    currentPage.value = page;
    filterServices();
  }
};


</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="text-center">
      <h1 class="text-4xl font-bold text-primary mt-4 mb-4">Buscar Servicios</h1>
      <div class="mx-auto max-w-md">
        <div class="mb-4">
          <label for="qFilter" class="block text-sm font-medium text-gray-700">Filtrar por:</label>
          <input type="text" id="qFilter" name="qFilter" v-model="qFilter" placeholder="Escribe aquí para filtrar"
            class="mt-1 p-2 border rounded-md w-full" />
        </div>

        <div class="mb-4">
          <label for="typeFilter" class="block text-sm font-medium text-gray-700">Filtrar por tipo de servicio:</label>
          <select v-model="typeFilter" class="mt-1 p-2 border rounded-md w-full">
            <option value="todos">Todos</option>
            <option value="analisis">Análisis</option>
            <option value="consultoria">Consultoría</option>
            <option value="desarrollo">Desarrollo</option>
          </select>
        </div>

        <button @click="filterServices" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Cargando...' : 'Filtrar' }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4" v-if=!loading>
        <div v-for="service in servicesList" :key="service.id" class="bg-white rounded-lg overflow-hidden shadow-md">
          <div class="p-4 cursor-pointer" @click="redirectToDetail(service.id)">
            <h2 class="text-lg font-bold text-gray-800">Institución: {{ service.laboratory }}</h2>
            <h2 class="text-lg font-bold text-gray-800">Servicio: {{ service.name }}</h2>
            <p class="text-sm text-gray-600">Descripcion: {{ service.description }}</p>
            <p class="text-sm text-gray-600">Tipo: {{ service.service_type }}</p>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <div v-if="Math.ceil(totalServices / perPage) > 0">
          <button class="btn btn-primary m-1" v-for="page in Math.ceil(totalServices / perPage)" :key="page"
            @click="changePage(page)"
            :class="{ 'bg-orange-600 text-orange-50': page === currentPage, 'bg-orange-200 text-zinc-800': page !== currentPage }">
            {{ page }}
          </button>
          <p class="text-center">Página {{ currentPage }} de {{ Math.ceil(totalServices / perPage) }}</p>
        </div>
        <div v-else-if="!loading" class="bg-white rounded-lg overflow-hidden shadow-md">
          <div class="p-4">
            <p class="text-lg font-bold text-gray-800">No se encontraron Servicios</p>
          </div>
        </div>
      </div>


    </main>
  </div>
</template>
