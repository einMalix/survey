<template>
<div>
    <div class="Overview" v-if="!PasswordOK">
        <select v-model="Course" v-on:change="onChangeSelect">
            <option disabled value="">Kurs auswählen </option>
            <option v-for="course in courses" :key="course"> {{ course[0] }}, {{ course[1] }}:
              {{ course[3].substring(0, 16) }} - {{ course[4].substring(0, 16) }} </option>
        </select>
        <table>
            <tbody v-for="survey in surveys" :key="survey">
                <tr v-if="Course.split(',')[0] == survey[3]"
                v-on:click="onClickListElemSurvey(survey[0])">
                  <td>{{ survey[1] }}</td>
                </tr>
                <tr v-if="showSurveyInfos && SurveyInfosID == survey[0]">
                  <td>{{ survey[2] }}</td>
                  <td><button v-on:click="onClickSurvey"
                  v-if="!hideSurveyButton">Beantworten</button>
                    <div v-if="showPasswordForm">
                      <form>
                        Passwort<input type="password" v-model="Password" autocomplete="off"/>
                      </form>
                    <br>
                    <button v-on:click="onSubmit(survey[0])">Bestätigen</button>
                    <button v-on:click="onCancel()">Abbrechen</button>
                    </div>
                  </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="Survey" v-if="PasswordOK">

      <div v-for="question in QuestionData" :key="question">
        <br>
        <p>{{question[1]}}</p>
        <form>
        <div v-for="answeroption in AnswerOptionData" :key="answeroption">
          <div v-if="question[2] == 'Einfach'">
          <div v-if="question[0] == answeroption[0]">
            <label>
            <input type="radio" v-bind:name="question[0]" v-bind:value="answeroption[2]">
            {{answeroption[1]}}</label>
          </div>
          </div>
          <div v-if="question[2] == 'Mehrfach'">
            <div v-if="question[0] == answeroption[0]">
              <label>
              <input type="checkbox" name="mehrfach" v-bind:value="answeroption[2]">
              {{answeroption[1]}}</label>
            </div>
          </div>
        </div>
        <div v-if="question[2] == 'Skala'">
              <input type="range" v-bind:name="question[0]"
              min="0" max="100" step="1" v-model="SkalaValue">
              {{SkalaValue}}
          </div>
        </form>
      </div>
      <br>
      <button v-on:click="SendAnswers(surveyID)">Absenden</button>
    </div>
</div>
</template>

<script>
import axios from 'axios';

const crypto = require('crypto');

export default {
  props: ['courses', 'surveys'],
  data() {
    return {
      Course: '',
      courseID: '',
      showSurveyInfos: false,
      SurveyInfosID: '',
      showPasswordForm: false,
      hideSurveyButton: false,
      Password: '',
      PasswordOK: false,
      QuestionData: '',
      AnswerOptionData: '',
      SelectedAnswers: [],
      surveyID: '',
      SkalaValue: 0,
    };
  },
  methods: {
    onClickListElemSurvey(surveyID) {
      if (this.SurveyInfosID === surveyID) {
        this.showSurveyInfos = !this.showSurveyInfos;
      } else {
        this.showSurveyInfos = true;
        this.SurveyInfosID = surveyID;
      }
    },
    onClickSurvey() {
      this.showPasswordForm = true;
      this.hideSurveyButton = true;
    },
    onCancel() {
      this.showPasswordForm = false;
      this.hideSurveyButton = false;
      this.Password = '';
    },
    onChangeSelect() {
      this.onCancel();
      this.showSurveyInfos = false;
    },
    onSubmit(surveyID) {
      const path = `http://localhost:5000/survey/password/${surveyID}`;
      const hashPW = crypto.createHash('sha1').update(this.Password).digest('hex');
      axios.post(path, {
        survey: surveyID,
        password: hashPW,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
          this.getQuestionData(surveyID);
          this.PasswordOK = true;
          this.surveyID = surveyID;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    getQuestionData(surveyID) {
      const path = `http://localhost:5000/survey/questions/${surveyID}`;
      axios.get(path)
        .then((res) => {
          this.QuestionData = res.data;
          this.getAnswerOptionData(surveyID);
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    getAnswerOptionData(surveyID) {
      const path = `http://localhost:5000/survey/answeroptions/${surveyID}`;
      axios.get(path)
        .then((res) => {
          this.AnswerOptionData = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    // eslint-disable-next-line
    CheckInputs(surveyID) {
      // eslint-disable-next-line
      for (const questionID in this.QuestionData) {
        const radios = document.getElementsByName(questionID[0]);
        // eslint-disable-next-line
        for (const radio in radios) {
          if (radio.type === 'radio' && !radio.checked) {
            return;
          }
        }
      }
    },
    SendAnswers(surveyID) {
      const inputs = document.getElementsByTagName('input');
      for (let i = 0; i < inputs.length; i += 1) {
        if ((inputs[i].type === 'radio' || inputs[i].type === 'checkbox') && inputs[i].checked) {
          this.SelectedAnswers.push(inputs[i].value);
        }
      }
      // eslint-disable-next-line
      for (const answeroption in this.AnswerOptionData) {
        if (this.SkalaValue >= 0 && this.SkalaValue <= 20) {
          if (this.AnswerOptionData[answeroption][1] === '0-20') {
            this.SelectedAnswers.push(this.AnswerOptionData[answeroption][2]);
          }
        } else if (this.SkalaValue >= 21 && this.SkalaValue <= 40) {
          if (this.AnswerOptionData[answeroption][1] === '20-40') {
            this.SelectedAnswers.push(this.AnswerOptionData[answeroption][2]);
          }
        } else if (this.SkalaValue >= 41 && this.SkalaValue <= 60) {
          if (this.AnswerOptionData[answeroption][1] === '40-60') {
            this.SelectedAnswers.push(this.AnswerOptionData[answeroption][2]);
          }
        } else if (this.SkalaValue >= 61 && this.SkalaValue <= 80) {
          if (this.AnswerOptionData[answeroption][1] === '60-80') {
            this.SelectedAnswers.push(this.AnswerOptionData[answeroption][2]);
          }
        } else if (this.SkalaValue >= 81 && this.SkalaValue <= 100) {
          if (this.AnswerOptionData[answeroption][1] === '80-100') {
            this.SelectedAnswers.push(this.AnswerOptionData[answeroption][2]);
          }
        }
      }
      const path = 'http://localhost:5000/survey/send';
      axios.post(path, {
        survey: surveyID,
        answers: this.SelectedAnswers,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
          window.location.reload();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.Overview {
  padding: 20px;
}
.Survey {
  padding: 20px;
}
</style>
