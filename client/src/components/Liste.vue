<template>
<div>
    <form>
    Vorname <input name="vorname" type="text" v-model="newVorname" />
    <br>
    Nachname <input name="nachname" type="text" v-model="newNachname" />
    <br>
    <button v-on:click="onSubmit()">Submit</button>
    </form>
    <br>
 <table>
    <thead>
    <tr>
        <th>ID</th>
        <th>Vorname</th>
        <th>Nachname</th>
    </tr>
    </thead>
    <tbody>
        <tr v-for="instructor in instructors" :key="instructor">
            <td>{{ instructor[0] }}</td>
            <td>{{ instructor[1] }}</td>
            <td>{{ instructor[2] }}</td>
            <td>
                <div>
                  <button type="button">Ändern</button>
                  <button type="button">Löschen</button>
                </div>
              </td>
        </tr>
    </tbody>
</table>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Liste',
  data() {
    return {
      instructors: '',
      newVorname: '',
      newNachname: '',
    };
  },
  methods: {
    getInstructors() {
      const path = 'http://localhost:5000/liste';
      axios.get(path)
        .then((res) => {
          this.instructors = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    addInstructor() {
      const path = 'http://localhost:5000/add';
      axios.post(path, {
        vorname: this.newVorname,
        nachname: this.newNachname,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
        }, (error) => {
        // eslint-disable-next-line
          console.log(error);
        });
    },
    onSubmit() {
      if (this.newVorname === '' || this.newNachname === '') {
      // eslint-disable-next-line
        console.error(error);
      } else {
        this.addInstructor();
      }
    },
  },
  created() {
    this.getInstructors();
  },
};
</script>
