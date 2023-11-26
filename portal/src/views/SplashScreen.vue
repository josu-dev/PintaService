<script setup>
  import IconLoader from '@/components/icons/IconLoader.vue';

  const props = defineProps({
    isLoading: {
      type: Boolean,
      default: true
    }
  });
</script>

<template>
  <main class="absolute inset-0 z-10" :class="{ fadeout: !props.isLoading }">
    <div class="flex flex-col items-center justify-center h-full bg-base-100">
      <div class="w-full flex flex-col gap-8 items-center">
        <img
          class="mx-auto max-w-[50%] animate-bounce"
          style="animation-duration: 1.25s"
          src="/logo_256x256.png"
          alt="Pinta Service Logo"
        />
        <h1
          class="flex flex-wrap justify-center text-xl md:text-3xl lg:text-5xl text-neutral-800 leading-normal font-bold text-center"
        >
          Cargando
          <IconLoader
            class="inline-flex stroke-[4] w-5 h-5 mt-2 md:w-7 md:h-7 md:mt-2 lg:w-9 lg:h-9 lg:mt-3 animate-spin ml-2"
          />
        </h1>
      </div>
    </div>
  </main>
</template>

<style scoped>
  .fadeout {
    animation: fadeout 0.5s forwards;
  }

  @keyframes fadeout {
    to {
      opacity: 0;
      visibility: hidden;
    }
  }
</style>
