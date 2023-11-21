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
      path: '/services/search',
      name:'services',
      component: () => import('../views/SearchServices.vue'),
    },
    {
      path:'/services/:service_id(\\d+)',
      props:true,
      name:'service',
      component: () => import('../views/ShowServiceView.vue'),
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
      path: '/stats',
      name: 'stats',
      component: () => import('../views/StatsView.vue'),
      meta: {
        requiresAuth: true,
        requiresSiteAdminOrInstitutionOwner: true
      }
    }
  ]
});

export default router;
