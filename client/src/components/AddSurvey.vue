<template>
<div class="AddSurvey">
    <form class="AddSurveyForm">
        <select v-model="AddCourse">
            <option disabled value="">Kurs auswählen </option>
            <option v-for="course in courses" :key="course"> {{ course[0] }}, {{ course[1] }}:
              {{ course[3].substring(0, 16) }} - {{ course[4].substring(0, 16) }} </option>
        </select>
        <br>
        Titel<input name="title" type="text" v-model="AddTitle" />
        <br>
        Beschreibung<input name="description" type="text" v-model="AddDescription" />
        <br>
        Passwort<input name="password" type="password" v-model="AddPassword" />
        <br>
        <questionbox @getQuestionList="onGetQuestionList"></questionbox>
        <br><br>
        <button v-on:click.prevent="onSubmit()">Hinzufügen</button>
    </form>
</div>
</template>

<script>
import axios from 'axios';

import QuestionBox from './QuestionBox.vue';

const crypto = require('crypto');

export default {
  props: ['courses'],
  components: {
    questionbox: QuestionBox,
  },
  data() {
    return {
      AddCourse: '',
      AddTitle: '',
      AddDescription: '',
      AddPassword: '',
      AddQuestions: [],
    };
  },
  methods: {
    AddSurvey() {
      const path = 'http://localhost:5000/survey/add';
      const hashPW = crypto.createHash('sha1').update(this.AddPassword).digest('hex');
      axios.post(path, {
        title: this.AddTitle,
        description: this.AddDescription,
        password: hashPW,
        courseID: this.AddCourse.split(',')[0],
        questionList: this.AddQuestions,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
          this.AddCourse = '';
          this.AddTitle = '';
          this.AddDescription = '';
          this.AddPassword = '';
          this.AddQuestions = '';
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit() {
      if (this.AddTitle === '' || this.AddDescription === '' || this.AddPassword === '' || this.AddCourse === '') {
      // eslint-disable-next-line
        console.error(error);
      } else {
        this.AddSurvey();
      }
    },
    onGetQuestionList(value) {
      this.AddQuestions = value;
    },
  },
};
</script>
