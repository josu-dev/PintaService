<script setup>
  import InputField from '@/components/form/InputField.vue';
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { ref } from 'vue';
  import { RouterLink, useRouter } from 'vue-router';

  const router = useRouter();
  const toastStore = useToastStore();
  const userStore = useUserStore();

  const form = ref({
    user: '',
    password: ''
  });

  /** @param {Event} event */
  async function submitLogin(event) {
    APIService.post('/auth', {
      body: {
        user: form.value.user,
        password: form.value.password
      },
      async onJSON(json) {
        /** @type {string} */
        const token = json.token;
        APIService.setJWT(token);

        const [user, isSiteAdmin, isInstitutionOwner] = await Promise.allSettled([
          APIService.get('/me/profile', { jwtError: 'throw' }),
          APIService.get('/me/rol/site_admin', { jwtError: 'throw' }),
          APIService.get('/me/rol/institution_owner', { jwtError: 'throw' })
        ]);
        if (
          user.status === 'rejected' ||
          isSiteAdmin.status === 'rejected' ||
          isInstitutionOwner.status === 'rejected'
        ) {
          toastStore.error('Error al iniciar sesión');
          return;
        }

        const is_site_admin = isSiteAdmin.value.data.is_site_admin;
        const is_institution_owner = isInstitutionOwner.value.data.is_institution_owner;

        userStore.setUser(user.value, {
          is_site_admin: is_site_admin,
          is_institution_owner: is_institution_owner
        });

        toastStore.success('Inicio de sesión exitoso');

        router.push({ name: 'home' });
      },
      onFailure(response) {
        toastStore.error('Error al iniciar sesión');
      },
      onError(error) {
        console.error('login error: ', error);
        toastStore.error('Error al iniciar sesión');
      }
    });
  }
</script>

<template>
  <main class="grid grid-rows-[1fr_2fr_2fr] h-full">
    <div class="row-start-2 w-full p-6 m-auto rounded-md lg:max-w-xl">
      <h1 class="text-4xl font-bold text-center text-primary">Inicio de Sesion</h1>
      <form
        class="flex flex-col items-center text-primary-content space-y-4 [&>:first-child]:mt-4 md:[&>:first-child]:mt-8"
        @submit.prevent="submitLogin"
      >
        <InputField
          type="email"
          name="user"
          label="Email"
          v-model:value="form.user"
          required
          autocomplete="email"
        />
        <InputField
          type="password"
          name="password"
          label="Contraseña"
          v-model:value="form.password"
          required
        />
        <button type="submit" class="btn btn-primary">Iniciar</button>
        <span class="text-secondary-content"
          >No tienes cuenta?
          <RouterLink to="/register" class="link link-hover font-semibold text-info"
            >Registrate</RouterLink
          ></span
        >
      </form>
    </div>
  </main>
</template>
