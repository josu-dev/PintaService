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

  const filterServices = () => {
    loading.value = true;
    const url = `/services/search?q=${qFilter.value}&type=${typeFilter.value}`;
    APIService.get(url, {
      onJSON(json) {
        servicesList.value = json.data;
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
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="text-center">
      <h1 class="text-4xl font-bold text-primary mt-4 mb-4">Buscar Servicios</h1>
      <div class="mx-auto max-w-md">
        <div class="mb-4">
          <label for="qFilter" class="block text-sm font-medium text-gray-700">Filtrar por:</label>
          <input
            type="text"
            id="qFilter"
            name="qFilter"
            v-model="qFilter"
            placeholder="Escribe aquí para filtrar"
            class="mt-1 p-2 border rounded-md w-full"
          />
        </div>

        <div class="mb-4">
          <label for="typeFilter" class="block text-sm font-medium text-gray-700"
            >Filtrar por tipo de servicio:</label
          >
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

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        <div
          v-for="service in servicesList"
          :key="service.id"
          class="bg-white rounded-lg overflow-hidden shadow-md"
        >
          <div class="p-4 cursor-pointer" @click="redirectToDetail(service.id)">
            <h2 class="text-lg font-bold text-gray-800">Institución: {{ service.laboratory }}</h2>
            <h2 class="text-lg font-bold text-gray-800">Servicio: {{ service.name }}</h2>
            <p class="text-sm text-gray-600">Descripcion: {{ service.description }}</p>
            <p class="text-sm text-gray-600">Tipo: {{ service.service_type }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
