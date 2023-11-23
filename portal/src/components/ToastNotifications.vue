<script setup>
  import IconInfo from '@/components/icons/IconInfo.vue';
  import IconMessage from '@/components/icons/IconMessage.vue';
  import IconThumsDown from '@/components/icons/IconThumbsDown.vue';
  import IconThumsUp from '@/components/icons/IconThumbsUp.vue';
  import IconWarning from '@/components/icons/IconWarning.vue';
  import IconX from '@/components/icons/IconX.vue';
  import { useToastStore } from '@/stores/toast';

  const toastStore = useToastStore();

  /** @type {Record<import('@/stores/toast').NotificationType, import('vue').Component>} */
  const iconMap = {
    success: IconThumsUp,
    error: IconThumsDown,
    info: IconInfo,
    warning: IconWarning,
    default: IconMessage
  };

  /** @type {Record<import('@/stores/toast').NotificationType, string>} */
  const alertClassMap = {
    success: 'alert alert-success',
    error: 'alert alert-error',
    info: 'alert alert-info',
    warning: 'alert alert-warning',
    default: 'alert'
  };
</script>

<template>
  <div class="toast toast-top toast-end z-10">
    <div
      v-for="notification in toastStore.notifications"
      v-bind:key="notification.id"
      :class="alertClassMap[notification.type]"
    >
      <div>
        <component :is="iconMap[notification.type]" class="mr-2" />
        <span>{{ notification.message }}</span>
      </div>

      <div v-if="notification.closeable" class="flex-none !mt-0">
        <button @click.prevent="toastStore.remove(notification)" aria-label="Close">
          <IconX />
        </button>
      </div>
    </div>
  </div>
</template>
