<script setup>
  const actionCards = [
    {
      id: 1,
      title: 'Listar',
      description: 'Lista de servicios prestados por cada institución',
      img: 'https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/68cedb8a-b2fa-4082-8b2b-52b747e6d7a1',
      link: '/services'
    },
    {
      id: 2,
      title: 'Buscar',
      description: 'Realizar búsqueda de servicios',
      img: 'https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/447700ab-c31f-45a2-8b11-6fbae78e5ed8',
      link: '/services/search'
    },
    {
      id: 3,
      title: 'Solicitar',
      description: 'Iniciar una solicitud de servicio',
      img: 'https://github.com/Fabian-Martinez-Rincon/Fabian-Martinez-Rincon/assets/55964635/68cedb8a-b2fa-4082-8b2b-52b747e6d7a1',
      link: '/services/search'
    }
  ];
</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="mx-auto p-4 my-8">
      <section class="flex flex-col justify-center p-6 items-center gap-8 mb-12">
        <div class="flex flex-col md:flex-row gap-8 items-center">
          <img class="mx-auto" src="/logo_256x256.png" alt="Pinta Service Logo" />
          <h1 class="text-4xl md:text-5xl leading-normal font-bold text-center">
            Bienvenido a <br />
            Pinta Service!
          </h1>
        </div>
        <p class="max-w-md text-xl mt-4 text-center text-balance text-neutral-700">
          Aquí puedes encontrar información sobre los servicios ofrecidos por nuestras instituciones
          asociadas y realizar solicitudes sobre los servicios que prestan
        </p>
      </section>

      <section class="p-6 my-12">
        <h2 class="text-2xl font-bold text-center md:text-3xl text-neutral-900">
          Que puedo hacer?
        </h2>
        <ul class="flex justify-center flex-wrap mt-6 xs:mt-12 gap-8 xs:gap-16">
          <template v-for="action in actionCards" :key="action.id">
            <li class="">
              <RouterLink
                :to="action.link"
                class="px-4 py-6 max-w-[20rem] h-full flex flex-col rounded-2xl ring-1 ring-primary outline-none transition-all duration-150 ease-in-out shadow-sm hover:bg-base-200/50 hover:scale-[1.04] hover:shadow-md focus:bg-base-200 focus:scale-105 focus:!ring-primary-focus focus:ring-2 focus:shadow-xl"
              >
                <figure class="grid place-items-center">
                  <img :src="action.img" :alt="action.title" class="w-1/3 rounded-xl" />
                </figure>
                <div class="flex-1 flex flex-col mt-4 items-center text-center">
                  <h3 class="text-2xl font-semibold">{{ action.title }}</h3>
                  <p class="text-lg mt-2">{{ action.description }}</p>
                </div>
              </RouterLink>
            </li>
          </template>
        </ul>
      </section>

      <section class="p-6 flex flex-col items-center my-12">
        <h2 class="text-2xl font-bold text-center md:text-3xl text-neutral-900">
          Información de contacto
        </h2>
        <address class="mt-4 xs:mt-8 text-lg leading-relaxed">
          <ul>
            <li>Dirección: Calle Principal, Ciudad</li>
            <li>Teléfono: +123456789</li>
            <li>Email: info@miportal.com</li>
          </ul>
        </address>
      </section>
    </main>
  </div>
</template>
