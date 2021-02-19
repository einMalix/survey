import { createWebHistory, createRouter } from 'vue-router';
import Liste from '../components/Liste.vue';
import Main from '../components/Main.vue';

const routes = [
  {
    path: '/liste',
    name: 'Liste',
    component: Liste,
  },
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
