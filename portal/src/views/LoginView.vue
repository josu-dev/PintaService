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
      onJSON(json) {
        if (json.result !== 'success') {
          toastStore.error('Error al iniciar sesión');
          return;
        }

        toastStore.success('Inicio de sesión exitoso');

        APIService.get('/me/profile', {
          onJSON(json) {
            userStore.setUser(json);

            router.push({ name: 'home' });
          }
        });
      },
      onFailure(response) {
        console.log(response);
        toastStore.error('Error al iniciar sesión');
      },
      onError(error) {
        console.log(error);
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
        <InputField type="email" name="user" label="Email" v-model:value="form.user" required />
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
