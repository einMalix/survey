<template>
<div>
    <p>Kursname: {{EvaluationCourse[1]}}</p>
    <p>Kursbeschreibung: {{EvaluationCourse[2]}}</p>
    <!-- eslint-disable-next-line -->
    <p>Zeitraum: {{EvaluationCourse[3].substring(0, 16)}} - {{EvaluationCourse[4].substring(0, 16)}}</p>

    <p>Umfragenname: {{EvaluationSurvey[1]}}</p>
    <p>Umfragenbeschreibung: {{EvaluationSurvey[2]}}</p>

    <dr/><dr/>
    <!-- Auswertung kommt hier hin -->
    <div v-for="question in QuestionsList" :key="question">
        <p>{{question[1]}}</p>
        <div v-for="answer in AnswerList" :key="answer">
            <p v-if="answer[0] == question[0]">{{answer[1]}} - {{answer[2]*100}}%</p>
        </div>
    </div>
    <dr/><dr/>
    <button v-on:click="OnClickReady">Fertig</button>
</div>
</template>

<script>
export default {
  props: ['EvaluationCourse', 'EvaluationSurvey', 'QuestionsList', 'AnswerList'],
  data() {
    return {
    };
  },
  methods: {
    OnClickReady() {
      this.$emit('changeShowOverview');
    },
  },
};
</script>
