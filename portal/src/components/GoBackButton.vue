<script setup>
  const { btnClass } = defineProps({
    btnClass: {
      type: String,
      default: 'btn-primary'
    }
  });

  function goBack() {
    window.history.back();
  }
</script>

<template>
  <button :class="'btn ' + btnClass" @click="goBack"><slot>Volver</slot></button>
</template>
