<script setup>
  import PaginationBar from '@/components/PaginationBar.vue';
  import { APIService } from '@/utils/api';
  import { ref, watch } from 'vue';

  const PER_PAGE = 1;
  /**
   * @typedef {Object} Institution
   * @property {number} id
   * @property {string} name
   * @property {string} information
   * @property {string} email
   */

  /** @type {import('vue').Ref<Institution[]>} */
  const institutions = ref([]);
  const loadingInstitutions = ref(false);
  const institutionsPage = ref(1);
  const institutionsPerPage = ref(PER_PAGE);
  const institutionsTotal = ref(0);

  /** @type {import('vue').Ref<Institution | undefined>} */
  const currentInstitution = ref();

  watch(
    institutionsPage,
    () => {
      loadingInstitutions.value = true;
      const url = `/enabled/institutions?page=${institutionsPage.value}&per_page=${institutionsPerPage.value}`;
      APIService.get(url, {
        onJSON(json) {
          institutions.value = json.data;
          institutionsPerPage.value = json.per_page;
          institutionsTotal.value = json.total + json.total + json.total;
        },
        afterRequest() {
          loadingInstitutions.value = false;
        }
      });
    },
    { immediate: true }
  );

  /**
   * @typedef {Object} Service
   * @property {number} id
   * @property {number} institution_id
   * @property {string} name
   * @property {string} description
   * @property {string} laboratory
   * @property {string} keywords
   * @property {boolean} enabled
   * @property {import('@/utils/enums').ServiceTypes} service_type
   */

  /** @type {import('vue').Ref<Service[] | undefined>} */
  const services = ref(undefined);

  const loadingServices = ref(false);
  const servicesPagination = ref({
    total: 0,
    page: 1,
    per_page: PER_PAGE
  });

  watch(currentInstitution, () => {
    if (!currentInstitution.value) {
      services.value = undefined;
      return;
    }
    loadingServices.value = true;
    const url = `/enabled/institutions/${currentInstitution.value.id}/services?page=${servicesPagination.value.page}&per_page=${servicesPagination.value.per_page}`;
    APIService.get(url, {
      onJSON(json) {
        services.value = json.data;
        servicesPagination.value = {
          total: json.total,
          page: json.page,
          per_page: json.per_page
        };
      },
      afterRequest() {
        loadingServices.value = false;
      }
    });
  });
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="flex flex-col gap-8 w-full p-2 py-4 md:py-8">
      <div class="mx-auto max-w-full">
        <h1 class="text-2xl font-semibold leading-relaxed">Servicios por Institucion</h1>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 place-items-center gap-8 mt-4 sm:pl-4">
          <section class="flex flex-col gap-2">
            <h2 v-if="loadingInstitutions" class="text-lg font-medium">Cargando instituciones</h2>
            <template v-else-if="!institutions.length">
              <h2 class="text-lg font-medium">No hay instituciones disponibles</h2>
            </template>
            <template v-else>
              <h2 class="text-lg font-medium">Instituciones</h2>
              <ul>
                <li
                  v-for="institution in institutions"
                  :key="institution.id"
                  class="flex flex-col gap-2"
                >
                  <div class="flex flex-row items-center justify-between">
                    <h2 class="text-lg font-medium">{{ institution.name }}</h2>
                    <button
                      class="text-sm text-blue-500 hover:text-blue-700"
                      @click="currentInstitution = institution"
                    >
                      Ver servicios
                    </button>
                  </div>
                  <p class="text-sm text-gray-500">{{ institution.information }}</p>
                </li>
              </ul>
            </template>
            <div class="mx-auto" :class="{ hidden: institutionsTotal === 0 }">
              <PaginationBar
                v-model:value="institutionsPage"
                :total="institutionsTotal"
                :per-page="institutionsPerPage"
                :loading="loadingInstitutions"
              />
            </div>
          </section>

          <section v-if="institutions.length" class="lg:col-span-2 flex flex-col gap-2">
            <h2 v-if="!currentInstitution" class="text-lg font-medium">
              Institucion no selecionada
            </h2>
            <template v-else-if="loadingServices">
              <h2 class="text-lg font-medium">
                Cargando servicios de {{ currentInstitution.name }}
              </h2>
            </template>
            <template v-else-if="!services?.length">
              <h2 class="text-lg font-medium">
                No hay servicios de {{ currentInstitution.name }} disponibles
              </h2>
            </template>
            <template v-else>
              <h2 class="text-lg font-medium">Servicios de {{ currentInstitution.name }}</h2>
              <div class="sm:pl-4">
                <ul>
                  <li v-for="service in services" :key="service.id" class="flex flex-col gap-2">
                    <h3 class="text-md font-medium">{{ service.name }}</h3>
                    <p class="text-sm text-gray-500">{{ service.description }}</p>
                  </li>
                </ul>
              </div>
            </template>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>
