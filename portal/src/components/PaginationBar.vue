<script setup>
  import IconLoader from '@/components/icons/IconLoader.vue';
  import { computed } from 'vue';

  const props = defineProps({
    value: {
      type: Number,
      default: 1
    },
    total: {
      type: Number,
      default: 0
    },
    perPage: {
      type: Number,
      default: 10
    },
    loading: {
      type: Boolean,
      default: false
    }
  });

  defineEmits(['update:value']);

  const MAXIMUN_PAGES = 5;

  const last = computed(() => Math.ceil(props.total / props.perPage));
  const pages = computed(() => {
    const pages = [];
    const totalPages = Math.ceil(props.total / props.perPage);
    const start = Math.max(1, props.value - Math.floor(MAXIMUN_PAGES / 2));
    const end = Math.min(totalPages, start + MAXIMUN_PAGES - 1);
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  });
</script>

<template>
  <div class="flex justify-center flex-wrap gap-2">
    <template v-if="(pages[0] ?? 0) > 1">
      <button class="btn btn-primary font-bold" @click="$emit('update:value', 1)" title="1">
        «
      </button>
    </template>
    <template v-for="page in pages" :key="page">
      <button
        v-if="page === props.value"
        class="btn pointer-events-none grid place-items-center relative"
      >
        <IconLoader class="animate-spin absolute" :class="{ hidden: !props.loading }" />
        <span :class="{ 'text-transparent': props.loading }">{{ page }}</span>
      </button>
      <button v-else class="btn btn-primary" @click="$emit('update:value', page)">
        {{ page }}
      </button>
    </template>
    <template v-if="(pages[pages.length - 1] ?? 0) < last">
      <button
        class="btn btn-primary font-bold"
        @click="$emit('update:value', last)"
        :title="last.toString()"
      >
        »
      </button>
    </template>
  </div>
</template>
