<template>
<div>
    <div class="navBar">
        <navBar></navBar>
    </div>
    <div class="login">
        <login></login>
        </div>
        <navBar @change_view="onClickHomeAdmin"/>
    <div class="liste" v-if='HomeAdminIsClicked'>
        <liste></liste>
    </div>
</div>
</template>

<script>
import Login from './Login.vue';
import NavBar from './NavBar.vue';
import Liste from './Liste.vue';

export default {
  name: 'Main',
  components: {
    login: Login,
    navBar: NavBar,
    liste: Liste,
  },
  data() {
    return {
      HomeAdminIsClicked: false,
    };
  },
  methods: {
    onClickHomeAdmin(value) {
      this.HomeAdminIsClicked = value;
    },

  },
  created() {

  },
};
</script>
