<template>
<div>
    <div v-if="loginOK" class="navBar">
        <navBar v-bind:userData="userData" @toggleViewHomeKursleiter="onClickHomeKursleiter"
        @toggleViewHomeAdmin="onClickHomeAdmin"></navBar>
    </div>
    <div class="login">
        <login @toggleViewUser="onLogin" @toggleUserData="onGetUserData"></login>
        </div>
    <div>
        <course v-if="HomeKursleiterIsClicked"></course>
        <liste v-if="HomeAdminIsClicked"></liste>
    </div>
    <br><br><br><br><br><br>
    <div class="user">
        <user v-bind:loginOK="loginOK" v-bind:userData="userData" v-if="loginOK"></user>
        </div>

      <p>{{userData}}</p>
</div>
</template>

<script>
import Login from './Login.vue';
import NavBar from './NavBar.vue';
import Liste from './Liste.vue';
import Course from './Course.vue';
import User from './User.vue';

export default {
  name: 'Main',
  components: {
    login: Login,
    navBar: NavBar,
    liste: Liste,
    course: Course,
    user: User,
  },
  data() {
    return {
      HomeAdminIsClicked: false,
      HomeKursleiterIsClicked: false,
      loginOK: false,
      userData: '',
    };
  },
  methods: {
    onClickHomeAdmin(value) {
      this.HomeKursleiterIsClicked = false;
      this.HomeAdminIsClicked = value;
    },
    onClickHomeKursleiter(value) {
      this.HomeAdminIsClicked = false;
      this.HomeKursleiterIsClicked = value;
    },
    onLogin(value) {
      this.loginOK = value;
    },
    onGetUserData(value) {
      this.userData = JSON.parse(value);
    },
  },
  created() {

  },
};
</script>
