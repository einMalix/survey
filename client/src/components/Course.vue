<template>
<div>
<div v-if="showOverview">
  <div class="AddCourse">
    <button v-on:click="onClickButtonAddCourse"
    v-if="hideAddCourseButton == false">Kurs hinzufügen</button>
    <form class="AddCourseForm" v-if="showAddCourseForm">
      Titel<input name="title" type="text" v-model="AddTitle" />
      <br>
      Beschreibung<input name="description" type="text" v-model="AddDescription" />
      <br>
      Startdatum<input name="datestart" type="date" v-model="AddDateStart" />
      <br>
      Enddatum<input name="dateend" type="date" v-model="AddDateEnd" />
      <br><br>
      <button v-on:click.prevent="AddCourseOnAdd">Hinzufügen</button>
      <button v-on:click="AddCourseOnCancel">Abbrechen</button>
    </form>
  </div>

    <table>
    <thead>
    <tr>
        <th>Titel</th>
        <th>Startdatum</th>
        <th>Enddatum</th>
    </tr>
    </thead>
    <tbody class="Course" v-for="course in courses" :key="course">
        <tr v-on:click="onClickListElemCourse(course[0])">
            <td>{{ course[1] }}</td>
            <td>{{ course[3].substring(0, 16) }}</td>
            <td>{{ course[4].substring(0, 16) }}</td>
        </tr>
        <tr class="CourseInfos" v-if="showCourseInfos && CourseInfosID == course[0]">
            <td>Beschreibung: {{ course[2] }}</td>
            <button v-if="hideEditButton == false" v-on:click="CourseOnEdit(course)">Ändern</button>
            <button v-if="hideDeleteButton == false" v-on:click="CourseOnDelete">Löschen</button>
            <div v-if="showEditForm">
              Titel<input name="title" type="text" v-model="EditTitle" />
              <br>
              Beschreibung<input name="description" type="text" v-model="EditDescription" />
              <br>
              Startdatum<input name="datestart" type="date"
              value="{{course[3]}} && new Date({{course[3]}}.getTime()-
              ({{course[3]}}.getTimezoneOffset()*60*1000)).toISOString().split('T')[0]"
              input="{{course[3]}} = $event.target.valueAsDate" />
              <br>
              Enddatum<input name="dateend" type="date"
              value="store.{{course[4]}}.toJSON().substring(0, 10)"
              input="store.{{course[4]}} = new Date($event)" />
              <br><br>
              <button v-on:click="CourseEditOnEdit(course[0])">Ändern</button>
              <button v-on:click="CourseEditOnCancel">Abbrechen</button>
            </div>
            <div v-if="showDeleteForm">
              <p>Wirklich löschen?</p>
              <br>
              <button v-on:click="CourseDeleteOnDelete(course[0])">Löschen</button>
              <button v-on:click="CourseDeleteOnCancel">Abbrechen</button>
            </div>
        </tr>
        <tr v-if="showCourseInfos && CourseInfosID == course[0]">
          <div v-for="survey in surveys" :key="survey">
            <table>
              <tbody>
                <tr v-if="course[0] == survey[3]" v-on:click="onClickListElemSurvey(survey[0])">
                  <td>{{ survey[1] }}</td>
                </tr>
                <tr v-if="showSurveyInfos && SurveyInfosID == survey[0]">
                  <td>{{ survey[2] }}</td>
                  <button v-if="hideEditSurveyButton == false"
                  v-on:click="SurveyOnEdit(survey)">Ändern</button>
                  <button v-if="hideDeleteSurveyButton == false"
                  v-on:click="SurveyOnDelete">Löschen</button>
                  <button v-on:click="SurveyOnEvaluation(course, survey)">Auswertung</button>
                  <div v-if="showEditSurveyForm">
                    Titel<input name="title" type="text" v-model="EditTitleSurvey" />
                    <br>
                    Beschreibung<input name="description" type="text"
                    v-model="EditDescriptionSurvey" />
                    <br>
                    Passwort<input name="password" type="password" v-model="EditPasswordSurvey" />
                    <br><br>
                    <button v-on:click="SurveyEditOnEdit(survey[0])">Ändern</button>
                    <button v-on:click="SurveyEditOnCancel">Abbrechen</button>
                  </div>
                  <div v-if="showDeleteSurveyForm">
                    <p>Wirklich löschen?</p>
                    <br>
                    <button v-on:click="SurveyDeleteOnDelete(survey[0])">Löschen</button>
                    <button v-on:click="SurveyDeleteOnCancel">Abbrechen</button>
                  </div>
                </tr>
              </tbody>
            </table>
          </div>
        </tr>
    </tbody>
    </table>
</div>
<div class="showEvaluation">
  <evaluation v-if="showOverview == false"
  v-bind:EvaluationCourse="EvaluationCourse" v-bind:EvaluationSurvey="EvaluationSurvey"
  @changeShowOverview="changeShowOverview" v-bind:QuestionsList="QuestionsList"
  v-bind:AnswerList="AnswerList" v-bind:ChartCheck="ChartCheck"></evaluation>
  </div>
</div>
</template>

<script>
import axios from 'axios';

import Evaluation from './Evaluation.vue';

const crypto = require('crypto');

export default {
  name: 'Course',
  components: {
    evaluation: Evaluation,
  },
  props: ['userData', 'courses', 'surveys'],
  data() {
    return {
      showOverview: true,
      showAddCourseForm: false,
      hideAddCourseButton: false,
      AddTitle: '',
      AddDescription: '',
      AddDateStart: '',
      AddDateEnd: '',
      showCourseInfos: false,
      showSurveyInfos: false,
      CourseInfosID: '',
      SurveyInfosID: '',
      showDeleteForm: false,
      hideDeleteButton: false,
      showDeleteSurveyForm: false,
      hideDeleteSurveyButton: false,
      EditTitle: '',
      EditDescription: '',
      EditDateStart: '',
      EditDateEnd: new Date().toISOString().slice(0, 10),
      showEditForm: false,
      hideEditButton: false,
      showEditSurveyForm: false,
      hideEditSurveyButton: false,
      EditTitleSurvey: '',
      EditDescriptionSurvey: '',
      EditPasswordSurvey: '',
      userLogin: this.userData.login,
      Questions: [],
      EvaluationCourse: '',
      EvaluationSurvey: '',
      QuestionsList: '',
      AnswerList: '',
      ChartCheck: false,

    };
  },
  filters: {
    truncate(text, length) {
      if (text.length > length) {
        return text.substring(0, length);
      }
      return text;
    },
  },
  methods: {
    changeShowOverview() {
      this.ChartCheck = false;
      this.showOverview = true;
    },
    onClickButtonAddCourse() {
      this.AddTitle = '';
      this.AddDescription = '';
      this.AddDateStart = '';
      this.AddDateEnd = '';
      this.showAddCourseForm = true;
      this.hideAddCourseButton = true;
    },
    AddCourseOnCancel() {
      this.showAddCourseForm = false;
      this.hideAddCourseButton = false;
    },
    AddCourseOnAdd() {
      if (this.AddTitle === '' || this.AddDateStart === '' || this.AddDateEnd === '') {
        // eslint-disable-next-line
        console.error('error');
      } else {
        this.AddCourse();
      }
    },
    AddCourse() {
      const path = 'http://localhost:5000/course/add';
      axios.post(path, {
        title: this.AddTitle,
        description: this.AddDescription,
        startdate: this.AddDateStart,
        enddate: this.AddDateEnd,
        instructor: this.userData.login,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
          this.$emit('getCourses');
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    onClickListElemCourse(courseID) {
      if (this.CourseInfosID === courseID) {
        this.showCourseInfos = !this.showCourseInfos;
      } else {
        this.showCourseInfos = true;
        this.CourseInfosID = courseID;
      }
      this.showDeleteForm = false;
      this.hideDeleteButton = false;
      this.showEditForm = false;
      this.hideEditButton = false;
      this.showSurveyInfos = false;
      this.SurveyInfosID = '';
    },
    onClickListElemSurvey(surveyID) {
      if (this.SurveyInfosID === surveyID) {
        this.showSurveyInfos = !this.showSurveyInfos;
      } else {
        this.showSurveyInfos = true;
        this.SurveyInfosID = surveyID;
      }
      this.showDeleteSurveyForm = false;
      this.hideDeleteSurveyButton = false;
      this.showEditSurveyForm = false;
      this.hideEditSurveyButton = false;
    },
    CourseOnDelete() {
      this.showDeleteForm = true;
      this.hideDeleteButton = true;
      this.hideEditButton = true;
    },
    CourseDeleteOnCancel() {
      this.showDeleteForm = false;
      this.hideDeleteButton = false;
      this.hideEditButton = false;
    },
    CourseDeleteOnDelete(courseID) {
      const path = `http://localhost:5000/course/delete/${courseID}`;
      axios.delete(path)
        .then(() => {
          this.$emit('getCourses');
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error)
        });
    },
    CourseOnEdit(course) {
      // eslint-disable-next-line
      const [courseID, courseTitle, courseDescription, courseStart, courseEnd] = course;
      this.EditTitle = courseTitle;
      this.EditDescription = courseDescription;
      this.EditDateStart = courseStart;
      this.EditDateEnd = courseEnd;
      this.showEditForm = true;
      this.hideEditButton = true;
      this.hideDeleteButton = true;
    },
    CourseEditOnCancel() {
      this.showEditForm = false;
      this.hideEditButton = false;
      this.hideDeleteButton = false;
    },
    CourseEditOnEdit(courseID) {
      if (this.EditTitle === '' && this.EditDescription === '' && this.EditDateStart === '' && this.EditDateEnd === '') {
        // eslint-disable-next-line
        console.error(error)
      } else {
        const path = `http://localhost:5000/course/edit/${courseID}`;
        axios.put(path, {
          title: this.EditTitle,
          description: this.EditDescription,
          startdate: this.EditDateStart,
          enddate: this.EditDateEnd,
        })
          .then(() => {
            this.$emit('getCourses');
            this.EditTitle = '';
            this.EditDescription = '';
            this.EditDateStart = '';
            this.EditDateEnd = '';
            this.showEditForm = false;
            this.hideEditButton = false;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    SurveyOnDelete() {
      this.showDeleteSurveyForm = true;
      this.hideDeleteSurveyButton = true;
      this.hideEditSurveyButton = true;
    },
    SurveyDeleteOnCancel() {
      this.showDeleteSurveyForm = false;
      this.hideDeleteSurveyButton = false;
      this.hideEditSurveyButton = false;
    },
    SurveyDeleteOnDelete(surveyID) {
      const path = `http://localhost:5000/survey/delete/${surveyID}`;
      axios.delete(path)
        .then(() => {
          this.$emit('getSurveys');
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error)
        });
    },
    SurveyOnEdit(survey) {
      // eslint-disable-next-line
      const [surveyID, surveyTitle, surveyDescription, surveyPassword] = survey;
      this.EditTitleSurvey = surveyTitle;
      this.EditDescriptionSurvey = surveyDescription;
      this.EditPasswordSurvey = '';
      this.showEditSurveyForm = true;
      this.hideEditSurveyButton = true;
      this.hideDeleteSurveyButton = true;
    },
    SurveyEditOnCancel() {
      this.showEditSurveyForm = false;
      this.hideEditSurveyButton = false;
      this.hideDeleteSurveyButton = false;
    },
    SurveyEditOnEdit(surveyID) {
      if (this.EditTitle === '' && this.EditDescription === '' && this.EditPasswordSurvey === '') {
        // eslint-disable-next-line
        console.error(error)
      } else {
        const path = `http://localhost:5000/survey/edit/${surveyID}`;
        const hashPW = crypto.createHash('sha1').update(this.EditPasswordSurvey).digest('hex');
        axios.put(path, {
          title: this.EditTitleSurvey,
          description: this.EditDescriptionSurvey,
          password: hashPW,
        })
          .then(() => {
            this.$emit('getSurveys');
            this.EditTitleSurvey = '';
            this.EditDescriptionSurvey = '';
            this.EditPasswordSurvey = '';
            this.showEditSurveyForm = false;
            this.hideEditSurveyButton = false;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    SurveyOnEvaluation(course, survey) {
      this.getEvaluation(survey[0]);
      this.EvaluationCourse = course;
      this.EvaluationSurvey = survey;
      this.ChartCheck = true;
      this.showOverview = false;
    },
    onGetQuestionList(value) {
      this.Questions = value;
    },
    getEvaluation(surveyID) {
      const path = `http://localhost:5000/evaluation/${surveyID}`;
      axios.get(path)
        // eslint-disable-next-line
        .then((res) => {
          // eslint-disable-next-line
          this.QuestionsList = res.data[0];
          // eslint-disable-next-line
          this.AnswerList = res.data[1];
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
  },
};
</script>

<style scoped>
.Course {
  border: 2px solid black;
  padding: 5px;
}

</style>
