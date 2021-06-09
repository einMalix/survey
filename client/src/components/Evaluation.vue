<template>
<div>
    <p>Kursname: {{EvaluationCourse[1]}}</p>
    <p>Kursbeschreibung: {{EvaluationCourse[2]}}</p>
    <!-- eslint-disable-next-line -->
    <p>Zeitraum: {{EvaluationCourse[3].substring(0, 16)}} - {{EvaluationCourse[4].substring(0, 16)}}</p>

    <p>Umfragenname: {{EvaluationSurvey[1]}}</p>
    <p>Umfragenbeschreibung: {{EvaluationSurvey[2]}}</p>

    <dr/><dr/>
    <div v-for="question in QuestionsList" :key="question">
        <p>{{question[1]}}</p>
        <div>
            <piechart v-bind:name="'chart' + question[0]"
            v-bind:piedata="createList(question[0])"></piechart>
        </div>
        <div v-for="answer in AnswerList" :key="answer">
            <p v-if="answer[0] == question[0]">{{answer[1]}} - {{answer[2]*100}}%</p>
        </div>
    </div>
    <dr/><dr/>
    <button v-on:click="OnClickReady">Fertig</button>
</div>
</template>

<script>
import Piechart from './Chart.vue';

export default {
  props: ['EvaluationCourse', 'EvaluationSurvey', 'QuestionsList', 'AnswerList', 'ChartCheck'],
  components: {
    piechart: Piechart,
  },
  data() {
    return {
      questioninfo: '',
      answeranswerlist: ['zu oberflächlich', 'adäquat', 'zu tief'],
      answeranswer: [0.25, 0.5, 0.25],
      state: {
        chartData: {
          datasets: [
            {
              data: [],
              backgroundColor: ['Red', 'Yellow', 'Blue', 'Green', 'Purple'],
            },
          ],
          labels: [],
        },
        chartOptions: {
          responsive: false,
        },
      },
    };
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
