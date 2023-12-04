<template>
    <div class="Signup">
      <h1>This is a Signup page</h1>
      <div class="container">
        <div class="row">
          <div class="col-sm"></div>
          <div class="col-sm">
            <form @submit.prevent="signup">
              <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input type="email" class="form-control" v-model="username" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
              </div>
              <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input type="password" class="form-control" v-model="password" id="exampleInputPassword1" placeholder="Password" />
              </div>
              <div class="form-group">
                <label for="exampleInputPassword2">Repeat Password</label>
                <input type="password" class="form-control" v-model="passwordRepeat" id="exampleInputPassword2" placeholder="Repeat password" />
              </div>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
          </div>
          <div class="col-sm"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { auth } from '@/firebase';
  
  export default {
    name: 'Signup',
    data() {
      return {
        username: '',
        password: '',
        passwordRepeat: '',
      };
    },
    methods: {
      signup() {
        if (this.password !== this.passwordRepeat) {
          console.error("Lozinke se ne podudaraju");
          return;
        }
  
        auth.createUserWithEmailAndPassword(this.username, this.password)
          .then(() => {
            console.log('Uspješna registracija');
          })
          .catch((error) => {
            console.error("Došlo je do pogreške", error);
          });
      },
    },
  };
  </script>