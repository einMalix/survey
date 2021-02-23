<template>
<div>
    <table>
    <thead>
    <tr>
        <th>Titel</th>
        <th>Startdatum</th>
        <th>Enddatum</th>
        <th>Kursleiter</th>
    </tr>
    </thead>
    <tbody>
        <tr v-for="course in courses" :key="course">
            <td>{{ course[0] }}</td>
            <td>{{ course[1] }}</td>
            <td>{{ course[2] }}</td>
            <td>{{ course[3] }}</td>
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
export default {
  name: 'Course',
  data() {
    return {
      courses: '',

    };
  },
  created() {

  },
};
</script>
