<template>
  <div id="app">
    <nav id="nav" class="navbar navbar-light navbar-expand-lg">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <img src="@/assets/logo_rukovnik.png" alt="Logo" height="80" class="d-inline-block align-text-top">
        </a>
        <div class="dropdown d-lg-none">
          <button class="navbar-toggler dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
            Menu
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/signup" class="nav-link">Signup</router-link>
            </li>
          </ul>
        </div>
        <button class="navbar-toggler d-none d-lg-block"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse d-lg-block" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li v-if="!store.currentUser" class="nav-item">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li v-if="!store.currentUser" class="nav-item">
              <router-link to="/signup" class="nav-link">Signup</router-link>
            </li>
            <li v-if="store.currentUser" class="nav-item">
              <a href="#" @click.prevent="logout()" class="nav-link">Logout</a>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input v-model="store.searchTerm"
                   class="form-control me-2"
                   type="search"
                   placeholder="Pretraga"
                   aria-label="Search">
          </form>
        </div>
      </div>
    </nav>

    {{ store.searchTerm }}

    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
import store from '@/store';
import { auth } from '@/firebase';
import router from '@/router';
import { getAuth, signOut } from 'firebase/auth'; // Dodano

auth.onAuthStateChanged((user) => {
  const currentRoute = router.currentRoute;
  console.log('Provjera stanja logina.');

  if (user) {
    console.log('***', user.email);
    store.currentUser = user.email;

    if (currentRoute.meta && currentRoute.meta.needsUser !== undefined && !currentRoute.meta.needsUser) {
      router.push({ name: 'home' });
    }
  } else {
    console.log('No user');
    store.currentUser = null;

    if (currentRoute.meta && currentRoute.meta.needsUser !== undefined && currentRoute.meta.needsUser) {
      router.push({ name: "login" });
    }
  }
});


export default {
  name: 'app',
  data() {
    return {
      store,
    };
  },
  methods: {
    logout() {
      const authInstance = getAuth(); // Dohvaćanje autentifikacijskog objekta
      signOut(authInstance)
       .then(() => {
        store.currentUser = null; // Postavljanje korisnika na null nakon odjave
       console.log('User signed out successfully');
       router.push({ name: 'login' });
        })
       .catch((error) => {
         console.error('Sign out error:', error);
       });
    },
  },
};
</script>


<style lang="scss">
.dropdown-menu {
  display: none;
}

.dropdown-menu.show {
  display: block;
}

#app {
  background-color: #FFEBEE;
  color: #C62828;
}

.navbar {
  background-color: #FFCDD2;
  color: #C62828;
}
.navbar-nav .nav-item .nav-link,
.dropdown-menu .nav-item .nav-link {
  color: #C62828;
}
.dropdown-menu .nav-item .nav-link:hover {
  color: #FF0000;
}
</style>