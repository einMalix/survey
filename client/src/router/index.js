import { createWebHistory, createRouter } from 'vue-router';
import Main from '../components/Main.vue';
import User from '../components/User.vue';

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
  {
    path: '/user',
    name: 'User',
    component: User,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
