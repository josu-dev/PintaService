import './assets/global.postcss';

import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import { useToastStore } from './stores/toast';
import { APIService } from './utils/api';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount('#app');

const toastStore = useToastStore();

APIService.onMaintenanceFailure = (response) => {
  toastStore.error('El servidor está en mantenimiento. Por favor, inténtelo de nuevo más tarde.');
};
