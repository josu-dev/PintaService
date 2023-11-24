<script setup>
  import PaginationBar from '@/components/PaginationBar.vue';
  import IconLoader from '@/components/icons/IconLoader.vue';
  import { useToastStore } from '@/stores/toast';
  import { APIService } from '@/utils/api';
  import { ref, watchEffect } from 'vue';
  import { RouterLink } from 'vue-router';

  const toastStore = useToastStore();

  const SEARCH_TIMEOUT = 1000;
  const searching = ref(false);
  let canScheduleSearch = true;
  let scheduledSearch = false;
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
  const searchedServices = ref([]);
  const searchQuery = ref('');
  const searchType = ref('todos');
  const autoSearch = ref(true);
  const serviceTypes = ref([]);

  let currentPage = ref(1);
  let perPage = ref(1);
  let totalServices = ref(0);

  /** @type {ReturnType<typeof setTimeout>} */
  let searchTimeout;

  APIService.get('/services_types', {
    onJSON(json) {
      serviceTypes.value = json.data;
    },
    onFailure(response) {
      console.error(response);
      toastStore.error('Error al buscar servicios');
    },
    onError(error) {
      console.error(error);
      toastStore.error('Error al buscar servicios');
    }
  });

  async function filterServices() {
    searching.value = true;
    const url = `/services/search?q=${searchQuery.value}&type=${searchType.value}&page=${currentPage.value}`;
    APIService.get(url, {
      onJSON(json) {
        searchedServices.value = json.data;
        currentPage.value = json.page;
        perPage.value = json.per_page;
        totalServices.value = json.total;
      },
      onFailure(response) {
        console.error(response);
        toastStore.error('Error al buscar servicios');
      },
      onError(error) {
        console.error(error);
        toastStore.error('Error al buscar servicios');
      },
      afterRequest() {
        searching.value = false;
      }
    });
  }

  const changePage = (page) => {
    if (page >= 1 && page <= Math.ceil(totalServices.value / perPage.value)) {
      currentPage.value = page;
      filterServices();
    }
  };

  watchEffect(() => {
    canScheduleSearch = autoSearch.value;
  });

  watchEffect(() => {
    searchQuery.value;
    searchType.value;
    currentPage.value = 1;
  });

  watchEffect(() => {
    searchQuery.value;
    searchType.value;
    if (!canScheduleSearch) return;
    scheduledSearch = true;

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      if (!scheduledSearch) return;
      scheduledSearch = false;
      filterServices();
    }, SEARCH_TIMEOUT);
  });

  function submitSearch(event) {
    if (canScheduleSearch && !scheduledSearch) return;
    if (searching.value) return;
    scheduledSearch = false;
    filterServices();
  }

  /** @type {Record<import('@/utils/enums').ServiceTypes, string>} */
  const serviceTypeBadge = {
    analisis: 'badge-info',
    consultoria: 'badge-warning',
    desarrollo: 'badge-success'
  };
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="p-4 text-center">
      <h1 class="text-4xl font-bold text-primary mt-4 mb-4">Buscar Servicios</h1>

      <div class="mx-auto max-w-md md:max-w-3xl">
        <form
          class="flex flex-col gap-y-4 mx-auto md:flex-row md:gap-x-4"
          @submit.prevent="submitSearch"
        >
          <div class="md:w-36">
            <label for="typeFilter" class="block text-lg font-medium text-gray-700"
              >Tipo de servicio:</label
            >
            <select v-model="searchType" class="mt-1 p-2 border rounded-md w-full capitalize">
              <option value="todos">Todos</option>
              <option v-for="type in serviceTypes" :key="type" :value="type" class="capitalize">
                {{ type }}
              </option>
            </select>
          </div>

          <div class="md:flex-1">
            <label for="qFilter" class="block text-lg font-medium text-gray-700">Buscar:</label>
            <input
              type="text"
              id="qFilter"
              name="qFilter"
              v-model="searchQuery"
              class="mt-1 p-2 border rounded-md w-full"
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block md:w-36 md:self-end">
            <template v-if="searching">
              <IconLoader class="animate-spin mr-1" />
              Buscando
            </template>
            <template v-else>Filtrar</template>
          </button>
        </form>
        <div class="form-control ml-auto w-max mt-2">
          <label class="label cursor-pointer gap-4">
            <span class="label-text">Busqueda automatica</span>
            <input type="checkbox" v-model="autoSearch" class="checkbox checkbox-primary" />
          </label>
        </div>
      </div>

      <div v-if="searching" class="mt-4">
        <p class="text-lg font-bold text-gray-800">Buscando servicios...</p>
      </div>
      <div v-else class="lg:px-8">
        <ul class="grid md:grid-cols-2 justify-center gap-4 mt-4">
          <template v-for="service in searchedServices" :key="service.id">
            <li class="flex-1 m-4">
              <RouterLink
                :to="`/services/${service.id}`"
                class="flex h-full py-3 px-4 shadow-md rounded-md bg-base-200/50 transition-all duration-200 hover:scale-105 hover:bg-base-200/75 hover:shadow-lg"
              >
                <div class="flex-1 flex flex-col items-center pb-5">
                  <div :class="`self-start badge ${serviceTypeBadge[service.service_type]}`">
                    {{ service.service_type }}
                  </div>
                  <h2 class="text-lg font-bold">{{ service.name }}</h2>
                  <h2 class="text-base mt-2 font-semibold">
                    Institución: {{ service.laboratory }}
                  </h2>
                  <p class="text-base mt-2 text-gray-600 max-w-[90%] text-balance">
                    {{ service.description }}
                  </p>
                </div>
              </RouterLink>
            </li>
          </template>
        </ul>

        <div class="mt-4" :class="{ hidden: totalServices === 0 }">
          <PaginationBar
            :value="currentPage"
            :total="totalServices"
            :per-page="perPage"
            :loading="searching"
            @update:value="changePage($event)"
          />
        </div>
      </div>
    </main>
  </div>
</template>
