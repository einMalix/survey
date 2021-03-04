<template>
<div>
    <div class="navBar">
        <navBar v-bind:userData="userData" v-bind:loginOK="loginOK"
        @toggleViewHomeKursleiter="onClickHomeKursleiter"
        @toggleViewHomeAdmin="onClickHomeAdmin"></navBar>
    </div>
    <div class="login">
        <login @updateUserLogin="onLogin" @toggleUserData="onGetUserData"></login>
        </div>
    <div>
        <course v-if="loginOK && HomeKursleiterIsClicked" v-bind:userData="userData"></course>
        <liste v-if="loginOK && HomeAdminIsClicked"></liste>
    </div>
</div>
</template>

<script>
import Login from './Login.vue';
import NavBar from './NavBar.vue';
import Liste from './Liste.vue';
import Course from './Course.vue';

export default {
  name: 'Main',
  components: {
    login: Login,
    navBar: NavBar,
    liste: Liste,
    course: Course,
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
      this.HomeAdminIsClicked = false;
      this.HomeKursleiterIsClicked = false;
    },
    onGetUserData(value) {
      this.userData = value;
    },
  },
  created() {

  },
};
</script>
