<script setup>

import InstitutionDetail from '@/components/showservice/InstitutionDetail.vue';
import ServiceDetail from '@/components/showservice/ServiceDetail.vue';
import LocationMap from '@/components/showservice/LocationMap.vue';
import GoBackButton from '@/components/GoBackButton.vue';
import { ref, defineProps } from 'vue';
import { APIService } from '@/utils/api';

const props = defineProps({
    service_id: String,
});

/**
 * @typedef {{
 *    name: string,
 *    description: string,
 *    laboratory: string,
 *    keywords: string[],
 *    enabled: boolean,
 * }} institutionData
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
 * }} serviceData
 */



const serviceData = ref([]);
const institutionData = ref([]);
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


</script>
<template>
    <div class="min-h-screen overflow-hidden mt-8">
        <main class="grid grid-cols-1 sm:grid-cols-2 gap-8 px-2 overflow-y-auto min-h-full">

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
            <div class="flex flex-col items-center justify-center mt-4  sm:mt-0">
                <div style="width: 100%; height: 500px;">
                    <LocationMap />
                </div>
                <button type="submit" class="btn btn-primary">Solicitar</button>
            </div>
        </main>
    </div>
</template>
  