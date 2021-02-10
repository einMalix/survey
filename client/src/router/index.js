import { createWebHistory, createRouter } from 'vue-router';
import Test from '../components/Test.vue';
import Instructor from '../components/Instructor.vue';
import Liste from '../components/Liste.vue';

const routes = [
  {
    path: '/liste',
    name: 'Liste',
    component: Liste,
  },
  {
    path: '/instructor',
    name: 'Instructor',
    component: Instructor,
  },
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
