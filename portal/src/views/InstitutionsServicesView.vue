<script setup>
  import PaginationBar from '@/components/PaginationBar.vue';
  import { APIService } from '@/utils/api';
  import { ref, watch } from 'vue';

  const PER_PAGE = 5;
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
          institutionsTotal.value = json.total;
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
  const servicesPage = ref(1);
  const servicesPerPage = ref(PER_PAGE);
  const servicesTotal = ref(0);

  watch([currentInstitution, servicesPage], () => {
    if (!currentInstitution.value) {
      services.value = undefined;
      return;
    }

    loadingServices.value = true;
    const url = `/enabled/institutions/${currentInstitution.value.id}/services?page=${servicesPage.value}&per_page=${servicesPerPage.value}`;
    APIService.get(url, {
      onJSON(json) {
        services.value = json.data;
        servicesPerPage.value = json.per_page;
        servicesTotal.value = json.total;
      },
      afterRequest() {
        loadingServices.value = false;
      }
    });
  });
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="flex flex-col px-2 py-4 md:py-8">
      <div class="mx-auto w-full">
        <h1 class="text-2xl md:text-3xl font-bold text-center text-primary leading-relaxed">
          Servicios por Institucion
        </h1>

        <div
          class="w-full grid md:grid-cols-2 lg:grid-cols-3 justify-items-center gap-8 my-4 sm:px-4"
        >
          <section class="col-start-1 w-full flex flex-col">
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
                    class="card card-compact bg-base-100 text-primary-content ring-1 ring-primary/50 shadow-md transition duration-150"
                    :class="{
                      '!ring-2 !ring-primary !shadow-lg': currentInstitution?.id === institution.id
                    }"
                  >
                    <div class="card-body">
                      <h3 class="card-title text-base md:text-lg">{{ institution.name }}</h3>
                      <p class="text-pretty line-clamp-4">
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

          <section class="lg:col-span-2 w-full flex flex-col">
            <header>
              <h2 class="text-lg md:text-xl font-medium">Servicios</h2>
              <p v-show="!currentInstitution" class="text-sm text-neutral-500">
                No hay institucion seleccionada
              </p>
              <p v-show="currentInstitution" class="text-sm text-neutral-500">
                Servicios de la institucion {{ currentInstitution?.name }}
              </p>
            </header>

            <div v-if="currentInstitution" class="my-4">
              <p
                v-show="loadingServices"
                class="flex justify-center items-center text-sm font-medium text-neutral-500"
              >
                Cargando servicios...
              </p>
              <p
                v-show="!loadingServices && !services?.length"
                class="flex justify-center items-center text-sm font-medium text-neutral-500"
              >
                No hay servicios de {{ currentInstitution.name }} disponibles
              </p>
              <ul
                v-show="!loadingServices && !!services?.length"
                class="flex flex-col gap-4 px-4 md:px-2"
              >
                <li v-for="service in services" :key="service.id">
                  <div
                    class="card card-compact bg-base-100 text-primary-content ring-1 ring-primary/50 shadow-md transition duration-150 hover:ring-2 hover:ring-primary hover:shadow-lg"
                  >
                    <div class="card-body">
                      <h3 class="card-title text-base md:text-lg">{{ service.name }}</h3>
                      <p class="text-pretty">
                        {{ service.description }}
                      </p>
                      <div class="card-actions justify-end">
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
              </ul>
            </div>

            <div class="mx-auto mt-4" :class="{ hidden: servicesTotal === 0 }">
              <PaginationBar
                v-model:value="servicesPage"
                :total="servicesTotal"
                :per-page="servicesPerPage"
                :loading="loadingServices"
              />
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>
