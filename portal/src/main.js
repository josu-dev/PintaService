import './assets/global.postcss';

import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router, { INITIAL_CLIENT_URL } from './router';
import { useSplashStore } from './stores/splashScreen';
import { useToastStore } from './stores/toast';
import { useUserStore } from './stores/user';
import { APIService } from './utils/api';
import { log } from './utils/logging';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount('#app');

const userStore = useUserStore();

router.beforeEach(async (to, from) => {
  if (to.meta.requiresAuth) {
    if (!userStore.user) {
      return { name: 'home' };
    }

    if (to.meta.requiresNormalUser && userStore.user.is_site_admin) {
      return { name: 'home' };
    }

    if (to.meta.requiresSiteAdminOrInstitutionOwner) {
      if (!userStore.user.is_site_admin && !userStore.user.is_institution_owner) {
        return { name: 'home' };
      }
    }
  } else if (to.meta.requiresNoAuth) {
    if (userStore.user) {
      return { name: 'home' };
    }
  }
});

const toastStore = useToastStore();

APIService.onMaintenanceError = (response) => {
  toastStore.error('El servidor está en mantenimiento. Por favor, inténtelo de nuevo más tarde.');
};

APIService.onJWTError = (response) => {
  toastStore.error('Su sesión ha expirado. Por favor, vuelva a iniciar sesión.');
  userStore.clearUser();
  APIService.clearJWT();
  router.push({ name: 'login' });
};

window.addEventListener('beforeunload', () => {
  APIService.saveJWTToLS();
});

const splashStore = useSplashStore();

if (APIService.setJWTFromLS()) {
  Promise.allSettled([
    APIService.get('/me/profile', { jwtError: 'throw' }),
    APIService.get('/me/rol/site_admin', { jwtError: 'throw' }),
    APIService.get('/me/rol/institution_owner', { jwtError: 'throw' })
  ])
    .then(([user, isSiteAdmin, isInstitutionOwner]) => {
      if (
        user.status === 'rejected' ||
        isSiteAdmin.status === 'rejected' ||
        isInstitutionOwner.status === 'rejected'
      ) {
        APIService.clearJWT();
        splashStore.initializing = false;
        return;
      }

      const is_site_admin = isSiteAdmin.value.data.is_site_admin;
      const is_institution_owner = isInstitutionOwner.value.data.is_institution_owner;

      userStore.setUser(user.value, {
        is_site_admin: is_site_admin,
        is_institution_owner: is_institution_owner
      });

      if (router.currentRoute.value.name === 'login') {
        router.push('/');
      } else if (router.currentRoute.value.path !== INITIAL_CLIENT_URL.pathname) {
        router.push(INITIAL_CLIENT_URL.pathname);
      }

      splashStore.initializing = false;
    })
    .catch((error) => {
      log.error('main', 'Error while initializing APIService: ', error);
      APIService.clearJWT();
      splashStore.initializing = false;
    });
} else {
  splashStore.enabled = false;
}
