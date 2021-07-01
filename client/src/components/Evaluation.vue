<template>
<div>
    <div class="description">
    <p>Kursname: {{EvaluationCourse[1]}}</p>
    <p>Kursbeschreibung: {{EvaluationCourse[2]}}</p>
    <!-- eslint-disable-next-line -->
    <p>Zeitraum: {{EvaluationCourse[3].substring(0, 16)}} - {{EvaluationCourse[4].substring(0, 16)}}</p>

    <p>Umfragenname: {{EvaluationSurvey[1]}}</p>
    <p>Umfragenbeschreibung: {{EvaluationSurvey[2]}}</p>
    </div>
    <div class="question" v-for="question in QuestionsList" :key="question">
        <h5>{{question[1]}} ({{question[3]}} Antwort/en)</h5>
        <div>
            <piechart v-bind:name="'chart' + question[0]"
            v-bind:piedata="createList(question[0])"></piechart>
        </div>
        <div v-for="answer in AnswerList" :key="answer">
            <p v-if="answer[0] == question[0]">{{answer[1]}} - {{answer[2]*100}}%</p>
        </div>
    </div>
    <button v-on:click="OnClickReady">Fertig</button>
</div>
</template>

<script>
import Piechart from './Chart.vue';

export default {
  props: ['EvaluationCourse', 'EvaluationSurvey', 'QuestionsList', 'AnswerList'],
  components: {
    piechart: Piechart,
  },
  methods: {
    OnClickReady() {
      this.$emit('changeShowOverview');
    },
    createList(question) {
      const data = {
        chartData: {
          datasets: [
            {
              data: [],
              backgroundColor: ['lightblue', 'tomato', 'lightgreen', 'darkviolet', 'sandybrown', 'gold', 'darkturquoise'],
              borderColor: 'lightgrey',
            },
          ],
          labels: [],
        },
        chartOptions: {
          responsive: false,
        },
      };
      // eslint-disable-next-line
      for (const answer of this.AnswerList.values()) {
        if (answer[0] === question) {
          data.chartData.labels.push(answer[1]);
          data.chartData.datasets[0].data.push(answer[2]);
        }
      }
      return data;
    },

  },
};
</script>

<style scoped>
.description {
  padding: 20px;
}

.question {
  padding: 20px;
}
</style>
