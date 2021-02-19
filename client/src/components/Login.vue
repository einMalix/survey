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
        Passwort <input name="password" type="text" v-model="Password" />
        <br>
        <button>Einloggen</button>
        <button v-on:click="onCancel">Abbrechen</button>
    </div>
</div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      showLoginForm: false,
      hideLoginButton: true,

    };
  },
  methods: {
    onCancel() {
      this.showLoginForm = !this.showLoginForm;
      this.hideLoginButton = !this.hideLoginButton;
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
