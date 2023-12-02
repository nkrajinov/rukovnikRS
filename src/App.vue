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
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/signup" class="nav-link">Signup</router-link>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input v-model="searchText"
                   class="form-control me-2"
                   type="search"
                   placeholder="Pretraga"
                   aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </nav>

    {{ searchText }}

    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      searchText: 'primjer2',
    };
  },
};
</script>

<style lang="scss">
/* Vaš postojeći stil */

/* Dodatni stil za dropdown izbornik */
.dropdown-menu {
  display: none;
}

.dropdown-menu.show {
  display: block;
}
</style>
