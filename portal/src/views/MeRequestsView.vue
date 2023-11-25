<script setup>
  import PaginationBar from '@/components/PaginationBar.vue';
  import { useToastStore } from '@/stores/toast';
  import { APIService } from '@/utils/api';
  import { requestStatus } from '@/utils/enums';
  import { ref, watch } from 'vue';

  const toastStore = useToastStore();
  /**
   * @typedef {{
   *  id: number,
   *  title: string,
   *  creation_date: string,
   *  close_date: string,
   *  status: import('@/utils/enums').RequestStatus,
   *  description: string,
   * }} ServiceRequest
   */

  /** @type {import('vue').Ref<ServiceRequest[]>} */
  const requests = ref([]);
  const loading = ref(false);
  const requestsPage = ref(1);
  /** @type {import('vue').Ref<number | undefined>} */
  const requestsPerPage = ref(undefined);
  const requestsTotal = ref(0);
  /** @type {import('vue').Ref<import('@/utils/enums').RequestStatus | 'Todos'>} */
  const filterRequestStatus = ref('Todos');
  /** @type {import('vue').Ref<'asc' | 'desc'>} */
  const filterRequestOrder = ref('desc');

  /** @type {{value: import('@/utils/enums').RequestStatus | 'Todos', label: string}[]} */
  const requestStatusOptions = [
    { value: 'Todos', label: 'Todos' },
    { value: requestStatus.ACCEPTED, label: 'Aceptada' },
    { value: requestStatus.REJECTED, label: 'Rechazada' },
    { value: requestStatus.IN_PROCESS, label: 'En proceso' },
    { value: requestStatus.FINISHED, label: 'Finalizada' },
    { value: requestStatus.CANCELED, label: 'Cancelada' }
  ];

  const requestStatusBadgeClasses = {
    [requestStatus.ACCEPTED]: 'badge-success',
    [requestStatus.REJECTED]: 'badge-error',
    [requestStatus.IN_PROCESS]: 'badge-primary',
    [requestStatus.FINISHED]: 'badge-info',
    [requestStatus.CANCELED]: 'badge-neutral'
  };

  watch(
    [requestsPage, filterRequestOrder, filterRequestStatus],
    () => {
      loading.value = true;

      let url = `/me/requests?page=${requestsPage.value}`;
      if (requestsPerPage.value) {
        url += '&per_page=' + requestsPerPage.value;
      }
      if (filterRequestStatus.value !== 'Todos') {
        url += '&status=' + filterRequestStatus.value;
      }
      url += '&order=' + filterRequestOrder.value;

      APIService.get(url, {
        onJSON(json) {
          requests.value = json.data;
          requestsPerPage.value = json.per_page;
          requestsTotal.value = json.total;
        },
        onFailure() {
          requests.value = [];
          requestsTotal.value = 0;
          toastStore.error('No se pudieron cargar las solicitudes');
        },
        onError() {
          requests.value = [];
          requestsTotal.value = 0;
          toastStore.error('No se pudieron cargar las solicitudes');
        },
        afterRequest() {
          loading.value = false;
        }
      });
    },
    { immediate: true }
  );
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="flex flex-col px-2 py-4 md:py-8">
      <h1 class="text-2xl md:text-3xl font-bold text-center text-primary leading-relaxed">
        Mis Solicitudes
      </h1>

      <div class="flex flex-wrap gap-4 justify-center my-4">
        <div class="w-full xs:max-w-[10rem]">
          <label for="filterRequestStatus" class="block text-lg font-medium text-gray-700"
            >Estado</label
          >
          <select
            v-model="filterRequestStatus"
            id="filterRequestStatus"
            name="filterRequestStatus"
            class="mt-1 p-2 border rounded-md w-full"
          >
            <template v-for="option in requestStatusOptions" :key="option.value">
              <option :value="option.value">
                {{ option.label }}
              </option>
            </template>
          </select>
        </div>
        <div class="w-full xs:max-w-[10rem]">
          <label for="filterRequestOrder" class="block text-lg font-medium text-gray-700">
            Orden de creacion
          </label>
          <select
            v-model="filterRequestOrder"
            id="filterRequestOrder"
            name="filterRequestOrder"
            class="mt-1 p-2 border rounded-md w-full"
          >
            <option value="desc">Descendente</option>
            <option value="asc">Ascendente</option>
          </select>
        </div>
      </div>

      <div class="my-4">
        <p
          v-show="loading"
          class="flex justify-center items-center text-sm font-medium text-neutral-500"
        >
          Cargando solicitudes...
        </p>
        <p
          v-show="!loading && requests.length === 0"
          class="flex justify-center items-center text-sm font-medium text-neutral-500"
        >
          {{
            filterRequestStatus === 'Todos'
              ? 'No has realizado solicitudes'
              : `No hay solicitudes con el estado ${filterRequestStatus}`
          }}
        </p>
        <ul
          v-show="!loading && requests.length > 0"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 px-4 md:px-2"
        >
          <li v-for="request in requests" :key="request.title">
            <div
              class="card card-compact bg-base-100 text-primary-content ring-1 ring-primary/50 shadow-md transition duration-150 hover:ring-2 hover:ring-primary hover:shadow-lg"
            >
              <div class="card-body">
                <h3 class="card-title text-base md:text-lg">{{ request.title }}</h3>
                <p class="text-pretty">
                  {{ request.description }}
                </p>
                <div class="card-actions justify-between">
                  <div class="badge self-center" :class="requestStatusBadgeClasses[request.status]">
                    {{ request.status }}
                  </div>
                  <RouterLink
                    :to="`/me/requests/${request.id}`"
                    class="btn btn-sm btn-primary normal-case"
                  >
                    Ver notas
                  </RouterLink>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <div class="mx-auto mt-4" :class="{ hidden: requestsTotal === 0 }">
        <PaginationBar
          v-model:value="requestsPage"
          :total="requestsTotal"
          :per-page="requestsPerPage"
          :loading="loading"
        />
      </div>
    </main>
  </div>
</template>
