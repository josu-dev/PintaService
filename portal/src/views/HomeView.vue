<!-- Home.vue -->

<script setup>
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
</script>

<template class="min-h-screen bg-slate-50 dark:bg-black dark:text-white" >
  <div class="h-full overflow-y-auto">
  <main class="container mx-auto p-4 max-w-full">
    <section id="home" class="flex flex-col-reverse justify-center sm:flex-row p-6 items-center gap-8 mb-12">
      <article>
        <img class="mx-auto" src="https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/eafc7e81-7f0d-4e82-893d-6b8ed026ea3f" alt="">
        <h2 class="max-w-md text-5xl font-bold text-center sm:text-slate-900">
          Bienvenido a Pinta Service!
        </h2>
        <p class="max-w-md text-2xl mt-4 text-center text-slate-700">
        Aquí puedes encontrar información sobre los servicios ofrecidos por nuestras instituciones y realizar solicitudes de servicio.
      </p>
      </article>
    </section>

    <section id="Acciones" class="p-6 my-12">
      <h2 class="text-4 font-bold text-center sm:text-4xl mb-6 text-slate-900">Acciones</h2>
      <ul class="list-none mx-auto my-12 flex flex-col sm:flex-row items-center gap-8">
        <li class="w-2/3 sm:5-6 flex flex-col items-center border border-solid border-slate-900 dark:border-black bg-white py-6 px-2 rounded-3xl shadow-xl">
          <h3 class="text-3xl text-center text-slate-900">Buscar</h3>
          <img class="w-1/2" src="https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/447700ab-c31f-45a2-8b11-6fbae78e5ed8" alt="">
          <p class="text-2xl text-center mt-2 text-slate-600">Realizar búsqueda de servicios.</p>
        </li>
        <li class="w-2/3 sm:5-6 flex flex-col items-center border border-solid border-slate-900 dark:border-black bg-white py-6 px-2 rounded-3xl shadow-xl">
          <h3 class="text-3xl text-center text-slate-900">Listar</h3>
          <br>
          <img class="w-1/2" src="https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/68cedb8a-b2fa-4082-8b2b-52b747e6d7a1" alt="">

          <p class="text-2xl text-center mt-2 text-slate-600">Lista de servicios prestados por cada institución.</p>
        </li>
        <li class="w-2/3 sm:5-6 flex flex-col items-center border border-solid border-slate-900 dark:border-black bg-white py-6 px-2 rounded-3xl shadow-xl">
          <h3 class="text-3xl text-center text-slate-900">Solicitar</h3>
          <br>
          <img class="w-1/2" src="https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/709374cf-ab6a-4dcc-baaf-65023b66036a" alt="">

          <p class="text-2xl text-center mt-2 text-slate-600">Iniciar una solicitud de servicio.</p>
        </li>
      </ul>
    </section>

    <section class="sm:5-6 flex flex-col items-center">
      <h2 class="text-4 font-bold text-center sm:text-4xl mb-6 text-slate-900">Información de contacto</h2>
      <address class="mt-2">
        <ul>
          <li>Dirección: Calle Principal, Ciudad</li>
          <li>Teléfono: +123456789</li>
          <li>Correo Electrónico: info@miportal.com</li>
        </ul>
    </address>

    </section>

  </main>
</div>
</template>

