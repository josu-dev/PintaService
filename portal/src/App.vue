<script setup>
  import LayoutHeader from '@/components/LayoutHeader.vue';
  import ToastNotifications from '@/components/ToastNotifications.vue';
  import { useSplashStore } from '@/stores/splashScreen';
  import SplashScreen from '@/views/SplashScreen.vue';
  import { RouterView } from 'vue-router';

  const splashStore = useSplashStore();
</script>

<template>
  <ToastNotifications />

  <SplashScreen v-if="splashStore.enabled" :is-loading="splashStore.initializing" />

  <header class="flex-none">
    <LayoutHeader />
  </header>

  <div class="flex-1 overflow-hidden">
    <RouterView />
  </div>
</template>
