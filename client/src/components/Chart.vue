<script>
import { Pie } from 'vue3-chart-v2';

export default {
  extends: Pie,
  props: {
    piedata: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.renderChart(this.piedata.chartData, this.piedata.chartOptions);
  },
};
</script>
