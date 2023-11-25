<script setup>
  import GoBackButton from '@/components/GoBackButton.vue';
  import MostEfficientInstitutions from '@/components/stats/MostEfficientInstitutions.vue';
  import MostRequestedServices from '@/components/stats/MostRequestedServices.vue';
  import RequestsPerStatus from '@/components/stats/RequestsPerStatus.vue';
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="flex flex-col gap-8 w-full p-2 py-4 md:py-8">
      <div class="mx-auto w-full max-w-[90%] lg:max-w-3xl">
        <h1 class="text-2xl font-semibold leading-relaxed">Estadisticas generales</h1>
        <div class="flex flex-col gap-8 lg:gap-16 mt-4 sm:pl-4">
          <section class="flex flex-col gap-2">
            <h2 class="text-lg font-medium">Solicitudes por estado</h2>
            <div class="sm:pl-4">
              <RequestsPerStatus />
            </div>
          </section>
          <section class="flex flex-col gap-2">
            <h2 class="text-lg font-medium">Servicios mas solicitados</h2>
            <div class="sm:pl-4 h-[24rem]">
              <MostRequestedServices />
            </div>
          </section>
          <section class="flex flex-col gap-2">
            <h2 class="text-lg font-medium">Instituciones mas efectivas</h2>
            <div class="sm:pl-4 h-[24rem]">
              <MostEfficientInstitutions />
            </div>
          </section>
        </div>

        <div class="flex justify-around gap-2 mt-8 md:mt-16">
          <GoBackButton class="btn-ghost bg-base-content bg-opacity-25 normal-case">
            Volver
          </GoBackButton>
        </div>
      </div>
    </main>
  </div>
</template>
