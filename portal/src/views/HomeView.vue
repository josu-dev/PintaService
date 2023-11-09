<script setup>
  import { useUserStore } from '@/stores/user';

  const userStore = useUserStore();
</script>

<template>
  <main>usuario: {{ userStore.user?.user }}</main>
</template>
