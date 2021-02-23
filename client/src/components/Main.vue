<template>
<div>
    <div class="navBar">
        <navBar></navBar>
    </div>
    <div class="login">
        <login></login>
        </div>
    <div>
        <navBar @toggleViewHomeKursleiter="onClickHomeKursleiter"
        @toggleViewHomeAdmin="onClickHomeAdmin"/>
        <course v-if="HomeKursleiterIsClicked"></course>
        <liste v-if="HomeAdminIsClicked"></liste>
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

  },
  created() {

  },
};
</script>
