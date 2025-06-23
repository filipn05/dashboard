<template>
  <div class="p-4">
    <h3 class="text-xl font-bold mb-4">Plot Subset/All</h3>
 
    <!-- Checkbox list -->
    <div class="mb-4 space-x-2">
      <label
        v-for="({ ds, col }) in allSeries"
        :key="ds + '|' + col"
        class="inline-flex items-center space-x-1"
      >
        <input
          type="checkbox"
          :value="{ ds, col }"
          v-model="selected"
        />
        <span>{{ col }}</span>
      </label>
    </div>

    <!-- Action buttons -->
    <div class="space-x-2">
      <button
        class="plot-btn"
        @click="plot"
        :disabled="!selected.length || loading"
      >
        {{ loading ? 'Loading…' : 'Plot Selected' }}
      </button>
      <button
        class="plot-btn"
        @click="plotAll"
        :disabled="loading"
      >
        {{ loading ? 'Loading…' : 'Plot All' }}
      </button>
    </div>

    <!-- Chart canvas -->
    <div class="mt-6">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {
  Chart,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
} from 'chart.js';

// Register Chart.js components
Chart.register(
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController
);

// A simple color palette for lines
const COLORS = [
  '#3366CC', '#DC3912', '#FF9900', '#109618',
  '#990099', '#0099C6', '#DD4477', '#66AA00',
  '#B82E2E', '#316395'
];

export default {
  name: 'PlotPanel',
  props: {
    datasets: { type: Object, required: true }
  },
  data() {
    return {
      selected: [],    // user‐picked series
      loading: false,
      chart: null      // Chart.js instance
    };
  },
  computed: {
    allSeries() {
      return Object.entries(this.datasets)
        .flatMap(([ds, meta]) =>
          meta.columns.map(col => ({ ds, col }))
        );
    }
  },
  methods: {
    // existing plot selected series
    async plot() {
      await this._plotSeries(this.selected);
    },

    // new: plot every series in the dataset collection
    async plotAll() {
      await this._plotSeries(this.allSeries);
    },

    // internal helper to fetch & render any list of { ds, col }
    async _plotSeries(seriesList) {
      if (!seriesList.length) return;
      this.loading = true;

      try {
        // fetch all series data in parallel
        const results = await Promise.all(
          seriesList.map(({ ds, col }) =>
            axios
              .post('/api/series-data', { dataset: ds, column: col })
              .then(res => ({ col, x: res.data.x, y: res.data.y }))
          )
        );

        // assume identical x for all
        const labels = results[0].x;

        // build Chart.js datasets
        const chartDatasets = results.map((s, idx) => ({
          label: s.col,
          data: s.y,
          fill: false,
          borderWidth: 2,
          tension: 0.2,
          borderColor: COLORS[idx % COLORS.length],
          pointBackgroundColor: COLORS[idx % COLORS.length]
        }));

        // destroy previous chart
        if (this.chart) this.chart.destroy();

        // render new chart
        this.chart = new Chart(this.$refs.chartCanvas, {
          type: 'line',
          data: { labels, datasets: chartDatasets },
          options: {
            responsive: true,
            plugins: { legend: { position: 'top' } },
            scales: {
              x: { title: { display: true, text: 'Index' } },
              y: { title: { display: true, text: 'Value' } }
            }
          }
        });

      } catch (e) {
        console.error(e);
        alert('Error loading series data');
      } finally {
        this.loading = false;
      }
    }
  },
  beforeUnmount() {
    if (this.chart) this.chart.destroy();
  }
};
</script>

<style scoped>
.plot-btn {
  background-color: #2563EB; /* blue-600 */
  color: white;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem; /* rounded-md */
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s, opacity 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.plot-btn:hover:not(:disabled) {
  background-color: #1D4ED8; /* blue-700 */
  transform: translateY(-1px);
}

.plot-btn:active:not(:disabled) {
  background-color: #1E40AF; /* blue-800 */
  transform: translateY(0);
}

.plot-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
