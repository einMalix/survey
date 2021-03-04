<template>
<div>
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
    <tbody v-for="course in courses" :key="course">
        <tr v-on:click="onClickListElem(course[0])">
            <td>{{ course[1] }}</td>
            <td>{{ course[3].substring(0, 16) }}</td>
            <td>{{ course[4].substring(0, 16) }}</td>
        </tr>
        <tr class="CourseInfos" v-if="showCourseInfos && CourseInfosID == course[0]">
            <p>Beschreibung: {{ course[2] }}</p>
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
    </tbody>
    </table>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Course',
  props: ['userData'],
  data() {
    return {
      courses: '',
      showAddCourseForm: false,
      hideAddCourseButton: false,
      AddTitle: '',
      AddDescription: '',
      AddDateStart: '',
      AddDateEnd: '',
      showCourseInfos: false,
      CourseInfosID: '',
      showDeleteForm: false,
      hideDeleteButton: false,
      EditTitle: '',
      EditDescription: '',
      EditDateStart: '',
      EditDateEnd: new Date().toISOString().slice(0, 10),
      showEditForm: false,
      hideEditButton: false,
      userLogin: this.userData.login,

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
    getCourses() {
      const path = `http://localhost:5000/course/list/${this.userLogin}`;
      axios.get(path)
        .then((res) => {
          this.courses = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
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
          this.getCourses();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    onClickListElem(courseID) {
      if (this.CourseInfosID === courseID) {
        this.showCourseInfos = !this.showCourseInfos;
      } else {
        this.showCourseInfos = true;
        this.CourseInfosID = courseID;
        this.showDeleteForm = false;
        this.hideDeleteButton = false;
        this.showEditForm = false;
        this.hideEditButton = false;
      }
    },
    CourseOnDelete() {
      this.showDeleteForm = true;
      this.hideDeleteButton = true;
    },
    CourseDeleteOnCancel() {
      this.showDeleteForm = false;
      this.hideDeleteButton = false;
    },
    CourseDeleteOnDelete(courseID) {
      const path = `http://localhost:5000/course/delete/${courseID}`;
      axios.delete(path)
        .then(() => {
          this.getCourses();
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
    },
    CourseEditOnCancel() {
      this.showEditForm = false;
      this.hideEditButton = false;
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
            this.getCourses();
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
  },
  created() {
    this.getCourses();
  },
};
</script>
