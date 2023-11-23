<script setup>
  import PaginationBar from '@/components/PaginationBar.vue';
  import { APIService } from '@/utils/api';
  import { ref, watch } from 'vue';

  const PER_PAGE = 2;
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
      <div class="mx-auto w-full">
        <h1 class="text-2xl md:text-3xl font-semibold leading-relaxed">
          Servicios por Institucion
        </h1>

        <div
          class="w-full grid md:grid-cols-2 lg:grid-cols-3 place-items-center gap-8 my-4 sm:pl-4"
        >
          <section class="col-start-1 w-full flex flex-col ring-1 ring-fuchsia-500">
            <header>
              <h2 class="text-lg md:text-xl font-medium">Instituciones</h2>
              <p class="text-sm text-neutral-500">
                Seleccione una institucion para ver sus servicios
              </p>
            </header>
            <div class="my-4">
              <p
                v-show="loadingInstitutions"
                class="flex justify-center items-center text-sm font-medium text-neutral-500"
              >
                Cargando instituciones...
              </p>
              <p
                v-show="!loadingInstitutions && institutions.length === 0"
                class="flex justify-center items-center text-sm font-medium text-neutral-500"
              >
                No hay instituciones disponibles
              </p>
              <ul
                v-show="!loadingInstitutions && institutions.length > 0"
                class="flex flex-col gap-4 px-4 md:px-2"
              >
                <li v-for="institution in institutions" :key="institution.id">
                  <div
                    class="card card-compact bg-base-100 text-primary-content ring-1 ring-primary/50 shadow-lg"
                    :class="{ '!ring-2': currentInstitution?.id === institution.id }"
                  >
                    <div class="card-body">
                      <h3 class="card-title text-base md:text-lg">{{ institution.name }}</h3>
                      <p class="text-pretty">
                        {{ institution.information }}
                      </p>
                      <div class="card-actions justify-end">
                        <button
                          class="btn btn-sm btn-primary normal-case"
                          @click="currentInstitution = institution"
                        >
                          Ver servicios
                        </button>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>

            <div class="mx-auto mt-4" :class="{ hidden: institutionsTotal === 0 }">
              <PaginationBar
                v-model:value="institutionsPage"
                :total="institutionsTotal"
                :per-page="institutionsPerPage"
                :loading="loadingInstitutions"
              />
            </div>
          </section>

          <section class="lg:col-span-2 flex flex-col gap-2 ring-1 ring-fuchsia-500">
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
