<script setup>
  import GoBackButton from '@/components/GoBackButton.vue';
  import InstitutionDetail from '@/components/showservice/InstitutionDetail.vue';
  import LocationMap from '@/components/showservice/LocationMap.vue';
  import ServiceDetail from '@/components/showservice/ServiceDetail.vue';
  import { APIService } from '@/utils/api';
  import { defineProps, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  const props = defineProps({
    service_id: String
  });
  const router = useRouter();
  const toastStore = useToastStore();
  const userStore = useUserStore();

  /**
   * @typedef {{
   *    name: string,
   *    description: string,
   *    laboratory: string,
   *    keywords: string[],
   *    enabled: boolean,
   * }} ServiceData
   */

  /**
   * @typedef {{
   *    name: string,
   *    information: string,
   *    address: string,
   *    web: string,
   *    keywords: string[],
   *    location: string,
   *    enabled: boolean,
   *    email: string,
   *    days_and_opening_hours: string,
   * }} InstitutionData
   */

  /** @type {import('vue').Ref<ServiceData>} */
  const serviceData = ref(/** @type {any} */ (null));

  /** @type {import('vue').Ref<InstitutionData>} */
  const institutionData = ref(/** @type {any} */ (null));
  const service_id = props.service_id ? props.service_id : '-1';

  APIService.get(`/service_institution/${service_id}`, {
    onJSON(json) {
      institutionData.value = json.data.institution;
      serviceData.value = json.data.service;
    },
    onFailure(response) {
      console.log('Request failed');
    },
    onError(error) {
      console.log(error);
    }
  });

  const redirectToRequest = () => {
    if (!service_id) return;
    if (!userStore.user) {
      toastStore.error('Debe iniciar sesión para solicitar un servicio');
      router.push('/login');
    } else {
      router.push(`/services/${service_id}/request`);
    }
  };
</script>
<template>
  <div class="h-full overflow-y-auto">
    <main class="grid grid-cols-1 sm:grid-cols-2 gap-8 px-2 mt-8">
      <!-- Service and institution detail -->
      <div>
        <GoBackButton />
        <h1 class="text-4xl font-bold text-center text-primary mb-4 mt-4">Servicio</h1>
        <div>
          <ServiceDetail :service="serviceData" />
        </div>
        <h1 class="text-4xl font-bold text-center text-primary mb-4">Institución</h1>
        <div>
          <InstitutionDetail :institution="institutionData" />
        </div>
      </div>

      <!-- Map and Location -->
      <div class="flex flex-col items-center justify-center mt-4 sm:mt-0">
        <div style="width: 100%; height: 500px">
          <LocationMap
            v-if="institutionData.location"
            :location="institutionData.location"
            :contact="institutionData.email"
          />
          <div v-else class="text-center text-gray-500">Cargando ubicación...</div>
        </div>
        <button type="submit" class="btn btn-primary" @click="redirectToRequest()">
          Solicitar
        </button>
      </div>
    </main>
  </div>
</template>
