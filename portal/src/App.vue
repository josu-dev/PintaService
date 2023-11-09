<script setup>
  import ToastNotifications from '@/components/ToastNotifications.vue';
  import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <ToastNotifications />

  <header class="flex-none">
    <div class="">
      <p>Pinta Service</p>

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/stats">Stats</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
      </nav>
    </div>
  </header>

  <div class="flex-1">
    <RouterView />
  </div>
</template>
