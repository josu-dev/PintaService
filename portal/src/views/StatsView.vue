<script setup>
  import MostEfficientInstitutions from '@/components/stats/MostEfficientInstitutions.vue'
  import MostRequestedServices from '@/components/stats/MostRequestedServices.vue'
  import RequestsPerStatus from '@/components/stats/RequestsPerStatus.vue'
</script>

<template>
  <div class="h-full overflow-hidden">
    <main class="flex flex-col gap-8 px-2 overflow-y-auto">
      <h1 class="text-2xl">Stats</h1>
      <section class="flex flex-col gap-2">
        <h2 class="text-lg">Requests per status</h2>
        <div>
          <RequestsPerStatus />
        </div>
      </section>
      <section class="flex flex-col gap-2">
        <h2 class="text-lg">Most requested services</h2>
        <div>
          <MostRequestedServices />
        </div>
      </section>
      <section class="flex flex-col gap-2">
        <h2 class="text-lg">Most efective institutions</h2>
        <div>
          <MostEfficientInstitutions />
        </div>
      </section>
    </main>
  </div>
</template>
