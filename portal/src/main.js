import './assets/global.postcss';

import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import { useToastStore } from './stores/toast';
import { useUserStore } from './stores/user';
import { APIService } from './utils/api';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount('#app');

const toastStore = useToastStore();

APIService.onMaintenanceFailure = (response) => {
  toastStore.error('El servidor está en mantenimiento. Por favor, inténtelo de nuevo más tarde.');
};

router.beforeEach(async (to, from) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth) {
    if (!userStore.user) {
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
