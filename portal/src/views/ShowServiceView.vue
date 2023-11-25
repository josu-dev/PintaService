<script setup>
  import GoBackButton from '@/components/GoBackButton.vue';
  import IconLoader from '@/components/icons/IconLoader.vue';
  import InstitutionDetail from '@/components/showservice/InstitutionDetail.vue';
  import LocationMap from '@/components/showservice/LocationMap.vue';
  import ServiceDetail from '@/components/showservice/ServiceDetail.vue';
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { log } from '@/utils/logging';
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';

  const props = defineProps({
    service_id: String
  });

  const loadingService = ref(true);
  const loadingInstitution = ref(true);

  const router = useRouter();
  const toastStore = useToastStore();
  const userStore = useUserStore();

  /**
   * @typedef {{
   *    name: string,
   *    description: string,
   *    laboratory: string,
   *    keywords: string,
   *    enabled: boolean,
   * }} DataService
   *
   * @typedef {{
   *    name: string,
   *    information: string,
   *    address: string,
   *    web: string,
   *    keywords: string,
   *    location: string,
   *    enabled: boolean,
   *    email: string,
   *    days_and_opening_hours: string,
   * }} DataInstitution
   */

  /** @type {import('vue').Ref<DataService>} */
  const dataService = ref(/** @type {any} */ (undefined));
  /** @type {import('vue').Ref<DataInstitution>} */
  const dataInstitution = ref(/** @type {any} */ (undefined));

  const service_id = parseInt(props.service_id || '1');

  APIService.get(`/services/${service_id}`, {
    onJSON(json) {
      dataService.value = json;
      loadingService.value = false;
    },
    onFailure(response) {
      log.warn('show service', 'failed to get service', response);
    },
    onError(error) {
      log.error('show service', 'error getting service', error);
    },
    afterRequest() {
      if (loadingService.value && !loadingInstitution.value) {
        log.warn('show service', 'failed to get service, going back');
        toastStore.warning('No se pudo obtener el servicio, intente mas tarde');
        router.back();
      } else {
        loadingService.value = false;
      }
    }
  });

  APIService.get(`/institution_of/${service_id}`, {
    onJSON(json) {
      dataInstitution.value = json;
      loadingInstitution.value = false;
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
      if (loadingInstitution.value && !loadingService.value) {
        log.warn('show service', 'failed to get institution, going back');
        toastStore.warning('No se pudo obtener la institucion, intente mas tarde');
        router.back();
      } else {
        loadingInstitution.value = false;
      }
    }
  });

  function goToServiceRequest() {
    if (!userStore.user) {
      toastStore.info('Inicia sesión para solicitar un servicio');
      router.push(`/login?redirect_to=/services/${service_id}/request`);
      return;
    }

    if (userStore.user.is_site_admin) {
      toastStore.info('No puedes solicitar un servicio siendo administrador del sitio');
      return;
    }

    router.push(`/services/${service_id}/request`);
  }
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="min-h-full flex flex-col px-2 py-4 md:py-8">
      <template v-if="loadingInstitution || loadingService">
        <div class="flex-1 grid place-items-center">
          <p
            class="text-lg md:text-xl flex flex-wrap max-w-[80%] justify-center text-balance items-center gap-2 font-semibold text-center text-neutral-800"
          >
            <IconLoader class="animate-spin inline-flex" />
            <span class="">Cargando informacion...</span>
          </p>
        </div>
      </template>

      <template v-else>
        <div class="flex-none flex flex-col justify-center items-center">
          <h1 class="text-2xl md:text-3xl font-bold text-center text-primary leading-relaxed">
            Detalle de Servicio
          </h1>
        </div>

        <div class="flex-1 grid md:grid-cols-2 gap-4 my-4 md:my-8 md:px-4 lg:px-8">
          <div class="flex flex-col gap-4 md:gap-8">
            <div>
              <h2 class="text-xl md:text-2xl font-bold text-center mb-2 mt-4">Servicio</h2>
              <div>
                <ServiceDetail :service="dataService" />
              </div>
            </div>
            <div>
              <h2 class="text-xl md:text-2xl font-bold text-center mb-2 mt-4">Institución</h2>
              <div>
                <InstitutionDetail :institution="dataInstitution" />
              </div>
            </div>
          </div>

          <div class="flex">
            <div style="width: 100%; height: 500px">
              <LocationMap :location="dataInstitution.location" :contact="dataInstitution.email" />
            </div>
          </div>

          <div
            class="md:col-span-2 self-start mx-auto flex flex-wrap-reverse justify-around gap-2 md:gap-8"
          >
            <GoBackButton class="btn-ghost bg-base-content bg-opacity-25 normal-case">
              Volver
            </GoBackButton>

            <template v-if="!userStore.user?.is_site_admin || dataService.enabled">
              <button class="btn btn-primary normal-case" @click="goToServiceRequest">
                Solicitar
              </button>
            </template>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>
