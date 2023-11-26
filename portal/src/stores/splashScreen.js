import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSplashStore = defineStore('routing', () => {
  const enabled = ref(true);
  const initializing = ref(true);

  return { enabled, initializing };
});
