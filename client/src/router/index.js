import { createWebHistory, createRouter } from 'vue-router';
import Liste from '../components/Liste.vue';

const routes = [
  {
    path: '/liste',
    name: 'Liste',
    component: Liste,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
