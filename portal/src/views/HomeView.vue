<script setup>
  import { useUserStore } from '@/stores/user';

  const userStore = useUserStore();
</script>

<template>
  <main>usuario: {{ userStore.user?.username }}</main>
</template>
