<template>
<div>
<div id="app">
  <div class="navbar">
    <div class="colum">
        <div v-if="userData.rolle == 'Administrator' && loginOK == true"
        class="HomeAdmin" @click="onClickHomeAdmin()">
            <p>Home Admin</p>
        </div>
      <div v-if="userData.rolle == 'Kursleiter' && loginOK == true"
      class="HomeKursleiter" @click="onClickHomeKursleiter()">
          <p>Home Kursleiter</p>
      </div>
      <div v-if="userData.rolle == 'Kursleiter' && loginOK == true"
      class="KursleiterFragen">
          <p>Kursleiter Fragen</p>
      </div>
    </div>
  </div>
</div>
    </div>
</template>

<script>
export default {
  name: 'NavBar',
  props: ['userData', 'loginOK'],
  data() {
    return {
      HomeAdminIsClicked: false,
      HomeKursleiterIsClicked: false,
      KursleiterFragenIsClicked: false,
    };
  },
  methods: {
    onClickHomeAdmin() {
      this.HomeKursleiterIsClicked = false;
      this.HomeAdminIsClicked = !this.HomeAdminIsClicked;
      this.$emit('toggleViewHomeAdmin', this.HomeAdminIsClicked);
    },
    onClickHomeKursleiter() {
      this.HomeAdminIsClicked = false;
      this.HomeKursleiterIsClicked = !this.HomeKursleiterIsClicked;
      this.$emit('toggleViewHomeKursleiter', this.HomeKursleiterIsClicked);
    },
  },
  created() {
  },
};
</script>

<style scoped>
.navbar{
  width: 80%;
  height: 60px;
  background-color: #192a56;
  top: 0;
  position: fixed;
  box-shadow: 0.1px 0.1px 15px 0.1px #273c75;
  border-radius:10px;
  display: flex;
}
.colum{
  display: flex;
  width: 95%;
  height: 40px;
  margin-top: 10px;
  margin-left: 10px;
  cursor: default;
}
.HomeAdmin{
  height: 34px;
  margin-left: 20px;
  display: flex;
  color: white;
  cursor: pointer;
}
.HomeKursleiter{
  height: 34px;
  margin-left: 20px;
  display: flex;
  color: white;
  cursor: pointer;
}
.KursleiterFragen{
  height: 34px;
  margin-left: 20px;
  display: flex;
  color: white;
  cursor: pointer;
}
</style>
