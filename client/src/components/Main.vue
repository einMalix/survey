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
        <survey v-if="loginOK == false" v-bind:courses="courseDataAll"
        v-bind:surveys="surveyDataAll"></survey>
        <course v-if="loginOK && HomeKursleiterIsClicked"
        v-bind:userData="userData" v-bind:courses="courseData" v-bind:surveys="surveyData"
        @getCourses="getCourses" @getSurveys="getSurveys"></course>
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
import Survey from './Survey.vue';

export default {
  name: 'Main',
  components: {
    login: Login,
    navBar: NavBar,
    liste: Liste,
    course: Course,
    addsurvey: AddSurvey,
    survey: Survey,
  },
  data() {
    return {
      HomeAdminIsClicked: false,
      HomeKursleiterIsClicked: false,
      UmfrageKursleiterIsClicked: false,
      loginOK: false,
      userData: '',
      courseData: '',
      surveyData: '',
      courseDataAll: '',
      surveyDataAll: '',
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
      this.UmfrageKursleiterIsClicked = false;
    },
    onGetUserData(value) {
      this.userData = value;
      this.getCourses();
    },
    getCourses() {
      const path = `http://localhost:5000/course/list/${this.userData.login}`;
      axios.get(path)
        .then((res) => {
          this.courseData = res.data;
          this.getSurveys();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    getCoursesAll() {
      const path = 'http://localhost:5000/course/list/all';
      axios.get(path)
        .then((res) => {
          this.courseDataAll = res.data;
          this.getSurveysAll();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    getSurveys() {
      const path = `http://localhost:5000/survey/list/${this.userData.login}`;
      axios.get(path)
        .then((res) => {
          this.surveyData = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    getSurveysAll() {
      const path = 'http://localhost:5000/survey/list/all';
      axios.get(path)
        .then((res) => {
          this.surveyDataAll = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getCoursesAll();
  },
};
</script>
