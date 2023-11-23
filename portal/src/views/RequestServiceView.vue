<script setup>
import InputField from '@/components/form/InputField.vue';
import { APIService } from '@/utils/api';
import { defineProps, ref } from 'vue';
import { useToastStore } from '@/stores/toast';
import { useRouter } from 'vue-router';

const props = defineProps({
    service_id: String
});
const router = useRouter();
const toastStore = useToastStore();

const service_id = props.service_id ? props.service_id : '-1';

const form = ref({
    title: '',
    description: ''
});
const loading = ref(false);
const submitForm = () => {
    loading.value = true;
    APIService.post('/me/requests', {
        body: {
            service_id: service_id,
            title: form.value.title,
            description: form.value.description
        },
        async onJSON(json) {
            toastStore.success('Servicio solicitado exitosamente');
            router.push(`/services/${service_id}`)
            loading.value = false;
        },
        onFailure(response) {
            toastStore.error('No se pudo solicitar el servicio, intente mas tarde');
        },
        onError(error) {
            console.log(error);
        }
    });
};
</script>

<template>
    <main class="flex flex-col items-center min-h-screen">
        <div>
            <h1 class="text-4xl font-bold text-primary mt-4 mb-4">Solicitar Servicio</h1>
            <form class="mx-auto max-w-md" @submit.prevent="submitForm">
                <InputField v-model:value="form.title" name="title" label="Titulo" required />
                <InputField v-model:value="form.description" name="description" label="Descripción" required />
                <div class="flex justify-center mt-4">
                    <button class='btn btn-primary' type="submit" :disabled="loading">
                        {{ loading ? 'Creando solicitud...' : 'Solicitar' }}</button>
                </div>
            </form>

        </div>
    </main>
</template>
