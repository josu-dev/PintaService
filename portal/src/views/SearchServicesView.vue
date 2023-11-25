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
   * }} ServiceData
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
    const rawQuery = searchQuery.value;
    const trimmedQuery = rawQuery.trim();
    if (!trimmedQuery && rawQuery !== '') {
      toastStore.info('La busqueda no pueden ser solo espacios');
      return;
    }

    searching.value = true;
    const url = `/services/search?q=${trimmedQuery}&type=${searchType.value}&page=${currentPage.value}`;
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
    <main class="px-2 py-4 md:py-8">
      <h1 class="text-2xl md:text-3xl font-bold text-center text-primary leading-relaxed">
        Buscar Servicios
      </h1>

      <div class="mx-auto max-w-md md:max-w-3xl mt-1 xs:mt-2">
        <form
          class="flex flex-col gap-y-2 md:gap-y-4 mx-auto md:flex-row md:gap-x-4"
          @submit.prevent="submitSearch"
        >
          <div class="md:w-36">
            <label for="searchType" class="block text-lg font-medium text-gray-700">
              Tipo de servicio
            </label>
            <select
              v-model="searchType"
              id="searchType"
              name="searchType"
              class="mt-1 p-2 border rounded-md w-full capitalize"
            >
              <option value="todos">Todos</option>
              <option
                v-for="serviceType in serviceTypes"
                :key="serviceType"
                :value="serviceType"
                class="capitalize"
              >
                {{ serviceType }}
              </option>
            </select>
          </div>

          <div class="md:flex-1 mt-auto">
            <label for="qFilter" class="block text-lg font-medium text-gray-700 md:sr-only">
              Buscar
            </label>
            <input
              type="text"
              id="qFilter"
              name="qFilter"
              v-model="searchQuery"
              class="mt-1 p-2 border rounded-md w-full"
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block md:w-36 md:self-end normal-case">
            <template v-if="searching">
              <IconLoader class="animate-spin mr-1" />
              Buscando
            </template>
            <template v-else>Filtrar</template>
          </button>
        </form>

        <div class="form-control ml-auto w-max mt-2">
          <label for="autoSearch" class="label cursor-pointer gap-4">
            <span class="label-text">Busqueda automatica</span>
            <input
              type="checkbox"
              v-model="autoSearch"
              id="autoSearch"
              name="autoSearch"
              class="checkbox checkbox-primary"
            />
          </label>
        </div>
      </div>

      <div v-if="searching" class="mt-4">
        <p class="text-lg font-medium text-center text-neutral-500">Buscando servicios...</p>
      </div>
      <div v-else-if="!searchedServices.length" class="mt-4">
        <p class="text-lg font-medium text-center text-neutral-500">No se encontraron servicios</p>
      </div>
      <div v-else class="lg:px-8">
        <ul class="grid md:grid-cols-2 justify-center gap-8 mt-4">
          <template v-for="service in searchedServices" :key="service.id">
            <li>
              <div
                class="card card-compact bg-base-100 text-primary-content ring-1 ring-primary/50 shadow-md transition duration-150 hover:ring-2 hover:ring-primary hover:shadow-lg"
              >
                <div class="card-body">
                  <h2 class="card-title text-lg font-semibold">
                    {{ service.name }}
                  </h2>
                  <p class="text-base font-semibold">Institucion: {{ service.laboratory }}</p>
                  <p class="text-pretty">
                    {{ service.description }}
                  </p>
                  <div class="card-actions justify-between">
                    <div :class="`badge self-center ${serviceTypeBadge[service.service_type]}`">
                      {{ service.service_type }}
                    </div>
                    <RouterLink
                      :to="`/services/${service.id}`"
                      class="btn btn-sm btn-primary normal-case"
                    >
                      Ver en detalle
                    </RouterLink>
                  </div>
                </div>
              </div>
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
