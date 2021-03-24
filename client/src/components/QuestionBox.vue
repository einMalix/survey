<template>
<div>
    <table>
        <tbody>
            <tr v-for="question in questions" :key="question">
                <td> <input v-on:change="sendQuestionList()"
                type="checkbox" :value="question[0]" v-model="questionList" /> </td>
                <td> {{ question[1] }} </td>
            </tr>
        </tbody>
    </table>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      questions: '',
      questionList: [],
    };
  },
  methods: {
    getQuestions() {
      const path = 'http://localhost:5000/questions/list';
      axios.get(path)
        .then((res) => {
          this.questions = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    sendQuestionList() {
      this.$emit('getQuestionList', this.questionList);
    },
  },
  created() {
    this.getQuestions();
  },
};
</script>
