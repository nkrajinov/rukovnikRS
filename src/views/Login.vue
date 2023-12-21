<template>
  <div class="login">
    <h1>Login Page</h1>
    <div class="container">
      <div class="row">
        <div class="col-sm"></div>
        <div class="col-sm">
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="email">Email address</label>
              <input type="email" v-model="email" class="form-control" id="email" placeholder="Enter email" required>
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input type="password" v-model="password" class="form-control" id="password" placeholder="Password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
          </form>
        </div>
        <div class="col-sm"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import { useRouter } from 'vue-router';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const auth = getAuth();
        const { email, password } = this;
        
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        // Uspješna prijava - preusmjeri korisnika na željenu stranicu (npr. Home)
        const router = useRouter();
        router.push({ name: 'Home' });
      } catch (error) {
        console.error('Login error:', error.message);
        // Ovdje možete dodati prikaz poruke o grešci korisniku
      }
    }
  }
};
</script>

<style scoped>
/* Stilizacija po želji */
.login {
  /* Stilizacija za login stranicu */
}
</style>

