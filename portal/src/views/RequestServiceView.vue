<script setup>
  import GoBackButton from '@/components/GoBackButton.vue';
  import InputField from '@/components/form/InputField.vue';
  import TextareaField from '@/components/form/TextareaField.vue';
  import IconLoader from '@/components/icons/IconLoader.vue';
  import { useToastStore } from '@/stores/toast';
  import { APIService } from '@/utils/api';
  import { log } from '@/utils/logging';
  import { defineProps, ref } from 'vue';
  import { useRouter } from 'vue-router';

  const props = defineProps({
    service_id: String
  });

  const router = useRouter();
  const toastStore = useToastStore();

  if (!props.service_id) {
    router.push('/');
  }

  const creatingRequest = ref(false);

  const form = ref({
    title: '',
    description: ''
  });

  function submitRequest(event) {
    if (creatingRequest.value) {
      return;
    }

    creatingRequest.value = true;

    APIService.post('/me/requests', {
      body: {
        service_id: props.service_id,
        title: form.value.title,
        description: form.value.description
      },
      async onJSON(json) {
        toastStore.success('Servicio solicitado exitosamente');
        router.push(`/services/${props.service_id}`);
      },
      onFailure(response) {
        log.warn('request service', 'failed to request service', response);
        toastStore.error('No se pudo solicitar el servicio, intente mas tarde');
      },
      onError(error) {
        log.error('request service', 'error requesting service', error);
        toastStore.error('No se pudo solicitar el servicio, intente mas tarde');
      },
      afterRequest() {
        creatingRequest.value = false;
      }
    });
  }
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="h-full flex flex-col px-2 py-4 md:py-8">
      <div class="flex-none flex flex-col justify-center items-center">
        <h1 class="text-2xl md:text-3xl font-bold leading-relaxed text-center">
          Solicitar Servicio
        </h1>
      </div>

      <div class="flex-1 flex flex-col my-4 md:my-8">
        <form
          class="flex flex-col gap-2 w-full max-w-[min(512px,90%)] mx-auto"
          @submit.prevent="submitRequest"
        >
          <InputField v-model:value="form.title" name="title" label="Titulo" required />
          <TextareaField
            v-model:value="form.description"
            name="description"
            label="Descripción"
            required
          />

          <div class="flex flex-wrap-reverse justify-around gap-2 md:gap-4 mt-4">
            <GoBackButton
              class="btn-ghost bg-base-content bg-opacity-10 normal-case"
              :disabled="creatingRequest"
            >
              Volver
            </GoBackButton>

            <button class="btn btn-primary normal-case" type="submit" :disabled="creatingRequest">
              <template v-if="creatingRequest">
                <IconLoader class="animate-spin mr-1 xs:mr-2" />
                Creando solicitud
              </template>
              <template v-else>Solicitar</template>
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>
