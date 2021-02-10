<template>
<div>
 <button type="button">Kursleiter hinzufügen</button>
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
    };
  },
  methods: {
    getMessage() {
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
  },
  created() {
    this.getMessage();
  },
};
</script>
