<template>
  <div class="about">
    <h1>This is a Login page</h1>
    <div class="container">
      <div class="row">
        <div class="col-sm"></div>
        <div class="col-sm">
          <form>
            <div class="form-group">
              <label for="exampleInputEmail1">Email address</label>
              <input type="email" v-model="username" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
              <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
              <label for="exampleInputPassword1">Password</label>
              <input type="password" v-model="password" class="form-control" id="exampleInputPassword1" placeholder="Password" />
            </div>
            <button type="button" @click="login()" class="btn btn-primary">Submit</button>
            <button v-if="loggedIn" @click="logout()" class="btn btn-danger">Logout</button> <!-- Dodan uvjetni prikaz gumba za logout -->
          </form>
        </div>
        <div class="col-sm"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { app } from '@/firebase';

export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
      loggedIn: false,
    };
  },
  methods: {
    login() {
      const auth = getAuth(app);

      signInWithEmailAndPassword(auth, this.username, this.password)
        .then((userCredential) => {
          const user = userCredential.user;
          console.log("Successful login", user);
          this.loggedIn = true; // Označite korisnika kao prijavljenog
          this.$router.push({ name: 'home' }); // Preusmjeri na početnu stranicu nakon uspješnog prijavljivanja
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    },
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
}
</script>
