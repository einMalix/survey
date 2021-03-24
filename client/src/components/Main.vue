<template>
<div>
    <div class="navBar">
        <navBar v-bind:userData="userData" v-bind:loginOK="loginOK"
        @toggleViewHomeKursleiter="onClickHomeKursleiter"
        @toggleViewHomeAdmin="onClickHomeAdmin"
        @toggleViewUmfrageKursleiter="onClickUmfrageKursleiter"></navBar>
    </div>
    <div class="login">
        <login @updateUserLogin="onLogin" @toggleUserData="onGetUserData"></login>
        </div>
    <div>
        <course v-if="loginOK && HomeKursleiterIsClicked"
        v-bind:userData="userData" v-bind:courses="courseData"
        @getCourses="getCourses"></course>
        <liste v-if="loginOK && HomeAdminIsClicked"></liste>
        <addsurvey v-if="loginOK && UmfrageKursleiterIsClicked"
        v-bind:courses="courseData"></addsurvey>
    </div>
</div>
</template>

<script>
import axios from 'axios';

import Login from './Login.vue';
import NavBar from './NavBar.vue';
import Liste from './Liste.vue';
import Course from './Course.vue';
import AddSurvey from './AddSurvey.vue';

export default {
  name: 'Main',
  components: {
    login: Login,
    navBar: NavBar,
    liste: Liste,
    course: Course,
    addsurvey: AddSurvey,
  },
  data() {
    return {
      HomeAdminIsClicked: false,
      HomeKursleiterIsClicked: false,
      UmfrageKursleiterIsClicked: false,
      loginOK: false,
      userData: '',
      courseData: '',
    };
  },
  methods: {
    onClickHomeAdmin(value) {
      this.HomeKursleiterIsClicked = false;
      this.HomeAdminIsClicked = value;
    },
    onClickHomeKursleiter(value) {
      this.UmfrageKursleiterIsClicked = false;
      this.HomeKursleiterIsClicked = value;
    },
    onClickUmfrageKursleiter(value) {
      this.HomeKursleiterIsClicked = false;
      this.UmfrageKursleiterIsClicked = value;
    },
    onLogin(value) {
      this.loginOK = value;
      this.HomeAdminIsClicked = false;
      this.HomeKursleiterIsClicked = false;
    },
    onGetUserData(value) {
      this.userData = value;
      this.getCourses();
    },
    getCourseData(value) {
      this.courseData = value;
    },
    getCourses() {
      const path = `http://localhost:5000/course/list/${this.userData.login}`;
      axios.get(path)
        .then((res) => {
          this.courseData = res.data;
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
