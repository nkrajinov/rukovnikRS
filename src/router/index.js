import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';
import store from '@/store';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      needsUser: true,
    },
  },
  {
    path: '/Login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/Signup',
    name: 'Signup',
    component: () => import('../views/Signup.vue')
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach( (to, from, next) =>{
  console.log("Stara ruta", from.name, " -> nova ruta", to.name, "korisnik", store.currentUser);
  
  const noUser = store.currentUser == null;
  if (noUser && to.meta.needsUser){
    next('login');
  }else{
    next();
  }
});

export default router;
