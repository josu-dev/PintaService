<script setup>
  const props = defineProps({
    btnClass: {
      type: String,
      default: 'btn-primary'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  });

  function goBack() {
    window.history.back();
  }
</script>

<template>
  <button :class="'btn ' + props.btnClass" :disabled="props.disabled" @click="goBack">
    <slot>Volver</slot>
  </button>
</template>
