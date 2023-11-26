<script setup>
  import InputField from '@/components/form/InputField.vue';
  import { BACKEND_BASE_URL } from '@/config';
  import { useToastStore } from '@/stores/toast';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { log } from '@/utils/logging';
  import { onMounted, ref } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const toastStore = useToastStore();
  const userStore = useUserStore();

  const isLogging = ref(false);

  const initialMail = String(router.currentRoute.value.query.email || '');
  const rawRedirectTo = router.currentRoute.value.query.redirect_to;
  const redirectTo = Array.isArray(rawRedirectTo) ? rawRedirectTo[0] : rawRedirectTo;

  const form = ref({
    user: initialMail,
    password: ''
  });

  /** @param {Event} event */
  async function submitLogin(event) {
    if (isLogging.value) {
      return;
    }
    isLogging.value = true;

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

        toastStore.success('Inicio de sesion exitoso');

        if (redirectTo) {
          router.push(`/${redirectTo.trim().slice(1)}`);
          return;
        }

        router.push('/');
      },
      onFailure(response) {
        if (response.status === 403) {
          toastStore.info('No puedes iniciar sesión en este momento');
          router.push('/account_disabled');
          return;
        }

        log.warn('login', 'failed to login', response);
        toastStore.error('Error al iniciar sesión');
      },
      onError(error) {
        log.error('login', 'error logging in', error);
        toastStore.error('Error al iniciar sesión');
      },
      afterRequest() {
        isLogging.value = false;
      }
    });
  }

  const registerLink = `${BACKEND_BASE_URL}/pre_register?redirect_to=${encodeURIComponent(
    window.location.href
  )}`;

  /** @type {import('vue').Ref<HTMLInputElement|null>} */
  const passwordInput = ref(null);

  onMounted(() => {
    if (initialMail) {
      passwordInput.value?.focus();
    }
  });
</script>

<template>
  <main class="grid grid-rows-[1fr_2fr_2fr] h-full">
    <div class="row-start-2 w-full p-4 m-auto rounded-md max-w-md">
      <h1 class="text-3xl md:text-4xl font-bold text-center text-primary leading-relaxed">
        Inicio de Sesion
      </h1>
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
          @ref:input="passwordInput = $event"
        />
        <button type="submit" class="btn btn-primary normal-case" :disabled="isLogging">
          Iniciar
        </button>
        <span class="text-secondary-content">
          No tienes cuenta?
          <a :href="registerLink" class="link link-hover font-semibold text-info">Registrate</a>
        </span>
      </form>
    </div>
  </main>
</template>
