<template>
  <div class="p-4">
    <h3 class="text-xl font-bold mb-4">Pairwise Comparison</h3>

    <!-- selectors identical to earlier -->
    <div class="mb-4">
      <label class="block mb-1 font-medium">Series A</label>
      <div class="flex space-x-2">
        <select v-model="selA.ds" class="border rounded px-2 py-1">
          <option disabled value="">Choose dataset…</option>
          <option v-for="(m, ds) in datasets" :key="ds" :value="ds">{{ m.name }}</option>
        </select>
        <select v-model="selA.col" class="border rounded px-2 py-1" :disabled="!selA.ds">
          <option disabled value="">Choose column…</option>
          <option v-for="col in datasets[selA.ds]?.columns||[]" :key="col" :value="col">{{ col }}</option>
        </select>
      </div>
    </div>

    <div class="mb-4">
      <label class="block mb-1 font-medium">Series B</label>
      <div class="flex space-x-2">
        <select v-model="selB.ds" class="border rounded px-2 py-1">
          <option disabled value="">Choose dataset…</option>
          <option v-for="(m, ds) in datasets" :key="ds" :value="ds">{{ m.name }}</option>
        </select>
        <select v-model="selB.col" class="border rounded px-2 py-1" :disabled="!selB.ds">
          <option disabled value="">Choose column…</option>
          <option v-for="col in datasets[selB.ds]?.columns||[]" :key="col" :value="col">{{ col }}</option>
        </select>
      </div>
    </div>

    <button
      class="action-btn"
      :disabled="!canPlot || loading"
      @click="plotPair"
    >
      {{ loading ? 'Computing…' : 'Plot A vs. B' }}
    </button>

    <div v-if="chart" class="mt-6">
      <canvas ref="canvas"></canvas>
    </div>

    <MetricsTable :metrics="metrics" />
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import axios from 'axios'
import {
  Chart, Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement, LineController
} from 'chart.js'
import MetricsTable from './MetricsTable.vue'

// register Chart.js components
Chart.register(
  Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement, LineController
)

// simple palette for two lines
const COLORS = ['#B82E2E', '#316395']

defineProps({ datasets: Object })
const selA = ref({ ds: '', col: '' })
const selB = ref({ ds: '', col: '' })
const chart = ref(null)
const metrics = ref(null)
const loading = ref(false)
const canvas = ref(null)

const canPlot = computed(() =>
  selA.value.ds && selA.value.col && selB.value.ds && selB.value.col
)

async function plotPair() {
  if (!canPlot.value) return
  loading.value = true
  metrics.value = null

  const [aRes, bRes] = await Promise.all([
    axios.post('/api/series-data', { dataset: selA.value.ds, column: selA.value.col }),
    axios.post('/api/series-data', { dataset: selB.value.ds, column: selB.value.col })
  ])

  const x = aRes.data.x
  const ya = aRes.data.y
  const yb = bRes.data.y

  if (chart.value) chart.value.destroy()
  chart.value = new Chart(canvas.value, {
    type: 'line',
    data: {
      labels: x,
      datasets: [
        {
          label: selA.value.col,
          data: ya,
          fill: false,
          borderWidth: 2,
          borderColor: COLORS[0],
          pointBackgroundColor: COLORS[0]
        },
        {
          label: selB.value.col,
          data: yb,
          fill: false,
          borderWidth: 2,
          borderColor: COLORS[1],
          pointBackgroundColor: COLORS[1]
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        x: { title: { display: true, text: 'Index' } },
        y: { title: { display: true, text: 'Value' } }
      }
    }
  })

  try {
    const res = await axios.post('/api/compare', { seriesA: ya, seriesB: yb })
    metrics.value = res.data
  } catch (e) {
    console.error(e)
    alert('Metrics calculation failed')
  } finally {
    loading.value = false
  }
}

onBeforeUnmount(() => {
  if (chart.value) chart.value.destroy()
})
</script>

<style scoped>
.action-btn {
  background-color: #2563EB; /* indigo-500 */
  color: white;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s, opacity 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Hover */
.action-btn:hover:not(:disabled) {
  background-color: #1D4ED8; /* indigo-600 */
  transform: translateY(-1px);
}

/* Active */
.action-btn:active:not(:disabled) {
  background-color: #1E40AF; /* indigo-700 */
  transform: translateY(0);
}

/* Disabled */
.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
