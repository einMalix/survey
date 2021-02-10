<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
    <form method="POST" action="">
    Vorname <input type="text" name="vorname" />
    <br>
    Nachname <input type="text" name="nachname" />
    <br>
    <input type="submit">
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Test',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    addInstructor(payload) {
      const path = 'http://localhost:5000/';
      axios.post(path, payload);
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        vorname: this.vorname,
        nachname: this.nachname,
      };
      this.addInstructor(payload);
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
