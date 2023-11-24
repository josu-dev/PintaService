import HomeView from '@/views/HomeView.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/services',
      name: 'services',
      component: () => import('../views/InstitutionsServicesView.vue')
    },
    {
      path: '/services/search',
      name: 'services_search',
      component: () => import('../views/SearchServicesView.vue')
    },
    {
      path: '/services/:service_id(\\d+)',
      props: true,
      name: 'service',
      component: () => import('../views/ShowServiceView.vue')
    },
    {
      path: '/services/:service_id(\\d+)/request',
      props: true,
      name: 'request',
      component: () => import('../views/RequestServiceView.vue'),
      meta: {
        requiresAuth: true,
        requiresNormalUser: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/me/requests',
      name: 'me_requests',
      component: () => import('../views/MeRequestsView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/me/requests/:request_id(\\d+)',
      name: 'me_request_notes',
      props: true,
      component: () => import('../views/RequestNotesView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/stats',
      name: 'stats',
      component: () => import('../views/StatsView.vue'),
      meta: {
        requiresAuth: true,
        requiresSiteAdminOrInstitutionOwner: true
      }
    },
    {
      path: '/account_disabled',
      name: 'account_disabled',
      component: () => import('../views/AccountDisabledView.vue'),
      meta: {
        requiresNoAuth: true
      }
    }
  ]
});

export default router;
