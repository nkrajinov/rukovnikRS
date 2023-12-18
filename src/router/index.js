import { createRouter, createWebHistory } from "vue-router";

import HomeView from '../views/HomeView.vue';
import EditNote from '../views/EditNote.vue'; // Pretpostavka da je EditNote.vue vaša komponenta za uređivanje bilješke
import store from '@/store';

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
  {
    path: '/edit-note/:id', // Definiramo rutu za uređivanje bilješke s dinamičkim ID-om
    name: 'EditNote',
    component: EditNote,
    meta: {
      needsUser: true, // Možete postaviti meta podatke prema potrebi
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes,
});

//listener koji nam omogućava kontrolu, ako se slažemo-ide na next
router.beforeEach((to, from, next) => {
  console.log("Stara ruta", from.name, " -> nova ruta", to.name, "korisnik", store.currentUser);

  const noUser = store.currentUser == null;

  if (to.meta && to.meta.needsUser && noUser) {
    // ako ruta zahtijeva autentikaciju i nema korisnika ulogiranog
    next('/login');
  } else {
    // ako ruta ne zahtijeva aut. tj.korisnik je ulogiran
    next();
  }
});

export default router;
