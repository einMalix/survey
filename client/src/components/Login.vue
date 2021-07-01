<template>
<div>
    <div class="logout" v-if="loginOK == true">
      <div v-show="hideLogoutButton">
        <button
          class="LogoutButton"
          type="button"
          v-on:click="showLogoutForm = !showLogoutForm;
          hideLogoutButton = !hideLogoutButton;">{{ userData.login }}
          </button>
    </div>
    <div v-show="showLogoutForm">
      <button v-on:click="onClickPassword">Passwort ändern</button><br>
    <div class="change_password" v-if="showPasswordForm">
        Altes Passwort <input name="old_password" type="password" v-model="Old_Password" />
        <br>
        Neues Passwort <input name="new_password_1" type="password" v-model="New_Password_1" />
        <br>
        Neues Passwort <input name="new_password_2" type="password" v-model="New_Password_2" />
        <br>
        <button v-on:click="onClickEditPassword">Ändern</button>
      </div>
      <button v-on:click="onLogout">Ausloggen</button><br>
      <button v-on:click="onCancelLogoutForm">Abbrechen</button>
    </div>
</div>
    <div class="login" v-else-if="loginOK == false">
    <div v-show="hideLoginButton">
        <button
            class="LoginButton"
            type="button"
            v-on:click="showLoginForm = !showLoginForm; hideLoginButton = !hideLoginButton;">Login
        </button>
    </div>
    <div v-show="showLoginForm">
      <form>
        Login <input name="login" type="text" v-model="Login" autocomplete="on" />
        <br>
        Passwort <input name="password" type="password" v-model="Password" autocomplete="off" />
        <br>
      </form>
        <button v-on:click="onLogin">Einloggen</button>
        <button v-on:click="onCancelLoginForm">Abbrechen</button>
    </div>
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
      showLogoutForm: false,
      hideLogoutButton: true,
      showPasswordForm: false,
      Login: '',
      Password: '',
      userData: '',
      Old_Password: '',
      New_Password_1: '',
      New_Password_2: '',
      loginOK: false,

    };
  },
  methods: {
    onCancelLoginForm() {
      this.showLoginForm = !this.showLoginForm;
      this.hideLoginButton = !this.hideLoginButton;
    },
    onCancelLogoutForm() {
      this.showPasswordForm = false;
      this.showLogoutForm = !this.showLogoutForm;
      this.hideLogoutButton = !this.hideLogoutButton;
    },
    onClickPassword() {
      this.showPasswordForm = !this.showPasswordForm;
      this.Old_Password = '';
      this.New_Password_1 = '';
      this.New_Password_2 = '';
    },
    onClickEditPassword() {
      const path = `http://localhost:5000/change_password/${this.userData.login}`;
      const hOldPassword = crypto.createHash('sha1').update(this.Old_Password).digest('hex');
      const hNewPassword1 = crypto.createHash('sha1').update(this.New_Password_1).digest('hex');
      const hNewPassword2 = crypto.createHash('sha1').update(this.New_Password_2).digest('hex');
      axios.put(path, {
        old_password: hOldPassword,
        new_password_1: hNewPassword1,
        new_password_2: hNewPassword2,
      });
      this.showPasswordForm = false;
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
          this.$emit('updateUserLogin', this.loginOK);
          this.onCancelLoginForm();
        })
        .catch((error) => {
          this.Password = '';
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onLogout() {
      const path = 'http://localhost:5000/logout';
      axios.post(path, {
        login: this.Login,
      });
      this.Login = '';
      this.Password = '';
      this.showPasswordForm = false;
      this.loginOK = false;
      this.$emit('updateUserLogin', this.loginOK);
    },
    getUserData(login) {
      const path = `http://localhost:5000/user/${login}`;
      axios.get(path)
        .then((res) => {
          this.userData = JSON.parse(res.data);
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
.logout{
    width: 20%;
    height: 60px;
    top: 0;
    right: 0;
    position: fixed;
    display: flex;
}
.LogoutButton{
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
