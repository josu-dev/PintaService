<script setup>
  import { useRouter } from 'vue-router';

  const router = useRouter();
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="h-full flex flex-col px-2 py-4 md:py-8">
      <div class="flex flex-col justify-center my-auto p-6 items-center gap-4 md:gap-8">
        <div class="flex flex-col md:flex-row gap-8 items-center">
          <img class="mx-auto max-w-[50%]" src="/logo_256x256.png" alt="Pinta Service Logo" />
          <div>
            <h1 class="text-4xl md:text-5xl !leading-snug font-bold text-center">
              <!-- <span class="text-primary">404</span><br /> -->
              Pagina no encontrada
            </h1>
            <p
              class="max-w-lg text-base xs:text-lg md:text-xl mt-8 text-center text-balance text-neutral-600"
            >
              La pagina
              <span class="font-bold text-neutral-700">'{{ router.currentRoute.value.path }}'</span>
              que buscas no existe
            </p>
          </div>
        </div>
      </div>
      <div class="mx-auto mt-auto">
        <RouterLink to="/" class="btn btn-primary mt-4 normal-case">Volver al Inicio</RouterLink>
      </div>
    </main>
  </div>
</template>
