import { createWebHistory, createRouter } from 'vue-router';
import Test from '../components/Test.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Test,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
