<script setup>
  import LayoutHeader from '@/components/LayoutHeader.vue';
  import ToastNotifications from '@/components/ToastNotifications.vue';
  import { RouterView } from 'vue-router';
</script>

<template>
  <ToastNotifications />

  <header class="flex-none">
    <LayoutHeader />
  </header>

  <div class="flex-1">
    <RouterView />
  </div>
</template>
