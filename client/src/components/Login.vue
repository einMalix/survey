<template>
<div class="login">
    <div v-show="hideLoginButton">
        <button
            class="LoginButton"
            type="button"
            v-on:click="showLoginForm = !showLoginForm; hideLoginButton = !hideLoginButton;">Login
        </button>
    </div>
    <div v-show="showLoginForm">
        Login <input name="login" type="text" v-model="Login" />
        <br>
        Passwort <input name="password" type="password" v-model="Password" />
        <br>
        <button v-on:click="onLogin">Einloggen</button>
        <button v-on:click="onCancel">Abbrechen</button>
    </div>
</div>
</template>

<script>
import axios from 'axios';

const crypto = require('crypto');

export default {
  name: 'Login',
  data() {
    return {
      showLoginForm: false,
      hideLoginButton: true,
      Login: '',
      Password: '',
      loginOK: false,
      userData: '',

    };
  },
  methods: {
    onCancel() {
      this.showLoginForm = !this.showLoginForm;
      this.hideLoginButton = !this.hideLoginButton;
    },
    onLogin() {
      const path = 'http://localhost:5000/login';
      const hashPW = crypto.createHash('sha1').update(this.Password).digest('hex');
      axios.post(path, {
        login: this.Login,
        password: hashPW,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
          this.loginOK = true;
          this.getUserData(this.Login);
          this.$emit('toggleViewUser', this.loginOK);
          this.onCancel();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    getUserData(login) {
      const path = `http://localhost:5000/user/${login}`;
      axios.get(path)
        .then((res) => {
          this.userData = res.data;
          this.$emit('toggleUserData', this.userData);
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },

  },
  created() {

  },
};
</script>

<style scoped>
.login{
    width: 20%;
    height: 60px;
    top: 0;
    right: 0;
    position: fixed;
    display: flex;
}
.LoginButton{
    position: relative;
    margin: auto;
    background-color: #192a56;
    box-shadow: 0.1px 0.1px 15px 0.1px #273c75;
    border-radius:10px;
}
button{
    color: white;
    background-color: #192a56;
}
</style>
