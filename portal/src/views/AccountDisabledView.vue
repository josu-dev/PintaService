<script setup></script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="h-full flex flex-col px-2 py-4 md:py-8">
      <div class="flex flex-col justify-center my-auto p-6 items-center gap-4 md:gap-8">
        <div class="flex flex-col md:flex-row gap-8 items-center">
          <img class="mx-auto max-w-[50%]" src="/logo_256x256.png" alt="Pinta Service Logo" />
          <h1 class="text-4xl md:text-5xl leading-normal font-bold text-center">Acceso Denegado</h1>
        </div>
        <p class="max-w-lg text-lg md:text-xl mt-4 text-center text-balance text-neutral-700">
          Tu cuenta ha sido deshabilitada por un administrador por lo que no puedes acceder a las
          funcionalidades que requieren iniciar sesión
        </p>
        <p class="max-w-lg text-lg md:text-xl mt-4 text-center text-balance text-neutral-700">
          Si crees que esto es un error, puedes solicitar la reactivación de tu cuenta al correo
          <span class="font-semibold">info@miportal.com</span>
        </p>
      </div>
      <div class="mx-auto mt-auto">
        <RouterLink to="/" class="btn btn-primary mt-4 normal-case">Volver al Inicio</RouterLink>
      </div>
    </main>
  </div>
</template>
