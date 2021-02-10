<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Kursleiter</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Kursleiter hinzufügen</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Vorname</th>
              <th scope="col">Nachname</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(instructor, index) in instructors" :key="index">
              <td>{{ instructor.ID }}</td>
              <td>{{ instructor.vorname }}</td>
              <td>{{ instructor.nachname }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Ändern</button>
                  <button type="button" class="btn btn-danger btn-sm">Löschen</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Instructor2',
  data() {
    return {
      instructors: [],
    };
  },
  methods: {
    getInstructors() {
      const path = 'http://localhost:5000/instructor';
      axios.get(path)
        .then((res) => {
          this.instructors = res.data.instructors;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getInstructors();
  },
};
</script>
