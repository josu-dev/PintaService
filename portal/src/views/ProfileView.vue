<script setup>
  import GoBackButton from '@/components/GoBackButton.vue';
  import { useUserStore } from '@/stores/user';
  import { computed } from 'vue';

  const userStore = useUserStore();

  const user = computed(() => {
    return (
      userStore.user ||
      /** @type {import("@/stores/user").User} */ ({
        username: '',
        email: '',
        address: '',
        document_number: '',
        document_type: 'DNI',
        gender_other: '',
        gender: 'Femenino',
        phone: '',
        is_institution_owner: false,
        is_site_admin: false
      })
    );
  });

  const userGender = computed(() => {
    if (user.value.gender === 'Otros(Por favor especifica)') {
      if (user.value.gender_other) {
        return '';
      }
      return user.value.gender_other;
    }
    return user.value.gender;
  });
</script>

<template>
  <div class="h-full overflow-hidden">
    <main class="flex flex-col gap-8 items-center h-full pt-8 md:pt-16 p-2 overflow-y-auto">
      <div>
        <div class="px-4 sm:px-0">
          <h1 class="text-2xl md:text-3xl font-bold text-primary leading-relaxed">
            Informacion de Perfil
          </h1>
          <p class="mt-1 max-w-2xl text-sm text-neutral-500 text-balance">
            Detalles personales de la cuenta para
            <span class="font-medium text-neutral-700">{{ user.username }}</span>
          </p>
        </div>
        <div class="mt-3">
          <dl class="divide-y divide-neutral-content">
            <div class="px-4 py-6 text-base sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt class="font-medium text-neutral-900">Nombre de usuario</dt>
              <dd class="mt-1 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ user.username }}
              </dd>
            </div>
            <div class="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt class="font-medium text-neutral-900">Correo electronico</dt>
              <dd class="mt-1 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ user.email }}
              </dd>
            </div>
            <div class="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt class="font-medium text-neutral-900">Direccion</dt>
              <dd class="mt-1 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ user.address }}
              </dd>
            </div>
            <div class="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt class="font-medium text-neutral-900">Documento</dt>
              <dd class="mt-1 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ user.document_type }} {{ user.document_number }}
              </dd>
            </div>
            <div class="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt class="font-medium text-neutral-900">Genero</dt>
              <dd class="mt-1 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ userGender }}
              </dd>
            </div>
            <div class="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt class="font-medium text-neutral-900">Telefono</dt>
              <dd class="mt-1 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ user.phone }}
              </dd>
            </div>
          </dl>
        </div>
      </div>
      <GoBackButton />
    </main>
  </div>
</template>
