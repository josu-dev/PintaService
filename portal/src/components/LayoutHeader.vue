<script setup>
  import IconLogin from '@/components/icons/IconLogin.vue';
  import IconMenu from '@/components/icons/IconMenu.vue';
  import IconPaintbrush from '@/components/icons/IconPaintbrush.vue';
  import IconSearch from '@/components/icons/IconSearch.vue';
  import IconStats from '@/components/icons/IconStats.vue';
  import IconUser from '@/components/icons/IconUser.vue';
  import { useUserStore } from '@/stores/user';
  import { APIService } from '@/utils/api';
  import { computed } from 'vue';
  import { RouterLink, useRouter } from 'vue-router';

  const router = useRouter();
  const userStore = useUserStore();

  function submitLogout() {
    APIService.clearJWT();
    userStore.clearUser();

    router.push({
      name: 'login'
    });
  }

  /**
   * @type {{
   *  label: string;
   *  path: string;
   *  icon: import('vue').Component;
   *  isRenderable?: import('vue').Ref<boolean>;
   * }[]} */
  const menuLinks = [
    {
      label: 'Estadisticas',
      path: '/stats',
      icon: IconStats,
      isRenderable: computed(
        () =>
          !!userStore.user && (userStore.user.is_site_admin || userStore.user.is_institution_owner)
      )
    },
    {
      label: 'Busqueda',
      path: '/services/search',
      icon: IconSearch
    },
    {
      label: 'Servicios',
      path: '/services',
      icon: IconPaintbrush
    }
  ];
</script>

<template>
  <div class="navbar shadow">
    <div class="navbar-start">
      <RouterLink to="/" class="btn btn-ghost normal-case text-xl">
        <div class="w-10 -ml-2">
          <img src="/logo_64x64.png" />
        </div>
        <span class="sr-only lg:not-sr-only ml-2">Pinta Service</span>
      </RouterLink>
    </div>

    <nav class="dropdown md:hidden">
      <label tabindex="0" class="btn btn-ghost w-max">
        <IconMenu class="sm:hidden" />
        <span class="sr-only sm:not-sr-only !ml-2 normal-case text-lg">Menu</span>
      </label>
      <ul
        tabindex="0"
        class="menu menu-sm dropdown-content -left-[calc(6.25rem-50%)] w-48 mt-3 z-[1] p-2 shadow bg-base-100 rounded-box"
      >
        <template v-for="link in menuLinks" :key="link.path">
          <li v-if="link.isRenderable?.value ?? true" class="">
            <RouterLink :to="link.path" :active-class="'active'" class="font-semibold">
              <component :is="link.icon" class="hidden xs:block" />
              <span class="">{{ link.label }}</span>
            </RouterLink>
          </li>
        </template>
      </ul>
    </nav>

    <nav class="navbar-center hidden md:flex">
      <ul class="menu menu-sm menu-horizontal px-1">
        <li v-for="link in menuLinks" :key="link.path" class="">
          <template v-if="link.isRenderable?.value ?? true">
            <RouterLink :to="link.path" :active-class="'active'" class="font-semibold">
              <component :is="link.icon" />
              <span class="sr-only lg:not-sr-only">{{ link.label }}</span>
            </RouterLink>
          </template>
        </li>
      </ul>
    </nav>

    <div class="navbar-end">
      <div v-if="!userStore.user" class="flex justify-center items-center">
        <RouterLink
          to="/login"
          :active-class="'!btn-primary btn-active'"
          class="btn btn-ghost normal-case text-lg"
        >
          <IconLogin class="sm:hidden" />
          <span class="sr-only sm:not-sr-only">Iniciar Sesion</span>
        </RouterLink>
      </div>
      <div v-else class="dropdown dropdown-end">
        <label tabindex="0" class="btn btn-ghost">
          <IconUser class="" />
          <span class="sr-only sm:not-sr-only !ml-2 normal-case text-lg">{{
            userStore.user.username
          }}</span>
          <!-- <span class="sr-only sm:not-sr-only normal-case text-lg">Menu</span> -->
        </label>
        <ul
          tabindex="0"
          class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-48"
        >
          <li class="sm:hidden">
            <div class="flex justify-between w-full">
              <span>{{ userStore.user.username }}</span>
            </div>
          </li>
          <div class="sm:hidden border-b border-neutral-content my-2"></div>
          <li>
            <RouterLink to="/profile" class="">Perfil</RouterLink>
          </li>
          <li>
            <form @submit.prevent="submitLogout"><button type="submit">Cerrar Sesion</button></form>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
