<script setup>
  import { useToastStore } from '@/stores/toast';
  const toastStore = useToastStore();

  const alertClassMap = {
    success: 'alert alert-success',
    error: 'alert alert-error',
    info: 'alert alert-info',
    warning: 'alert alert-warning',
    default: 'alert'
  };
</script>

<template>
  <div class="toast toast-top toast-end">
    <div
      v-for="notification in toastStore.notifications"
      v-bind:key="notification.id"
      :class="alertClassMap[notification.type]"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="stroke-primary shrink-0 w-6 h-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        ></path>
      </svg>
      <span>{{ notification.message }}</span>

      <div v-if="notification.closeable">
        <button
          @click.prevent="toastStore.remove(notification)"
          class="btn btn-sm"
          aria-label="Close"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>
