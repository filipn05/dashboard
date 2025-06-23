<template>
  <div class="p-4 mb-8 border rounded">
    <h3 class="text-xl font-bold mb-4">Trimming &amp; Sliding-Window Analysis</h3>

    <!-- Dataset & Column selectors -->
    <div class="mb-4 grid grid-cols-2 gap-4">
      <div>
        <label class="block font-medium mb-1">Dataset</label>
        <select v-model="sel.ds" class="w-full border rounded px-2 py-1">
          <option disabled value="">Choose…</option>
          <option v-for="(m, ds) in datasets" :key="ds" :value="ds">
            {{ m.name }}
          </option>
        </select>
      </div>
      <div>
        <label class="block font-medium mb-1">Column</label>
        <select v-model="sel.col" class="w-full border rounded px-2 py-1" :disabled="!sel.ds">
          <option disabled value="">Choose…</option>
          <option v-for="c in datasets[sel.ds]?.columns || []" :key="c" :value="c">
            {{ c }}
          </option>
        </select>
      </div>
    </div>

    <!-- Trim inputs -->
    <div class="mb-4 grid grid-cols-2 gap-4">
      <div>
        <label class="block font-medium mb-1">Start index</label>
        <input type="number" v-model.number="trim.start" min="0" class="w-full border rounded px-2 py-1" />
      </div>
      <div>
        <label class="block font-medium mb-1">End index</label>
        <input type="number" v-model.number="trim.end" :max="fullSeries.length-1" class="w-full border rounded px-2 py-1" />
      </div>
    </div>

    <button
      class="btn btn-success mb-6"
      :disabled="!canTrim || loading"
      @click="applyTrim"
    >
      {{ loading ? 'Processing…' : 'Apply Trim & Plot' }}
    </button>

    <!-- Trimmed plot -->
    <div v-if="trimmedData" class="mb-8">
      <h4 class="font-semibold mb-2">Trimmed Series</h4>
      <canvas ref="trimCanvas"></canvas>
    </div>

    <!-- Sliding-window controls -->
    <div class="mb-4 grid grid-cols-2 gap-4">
      <div>
        <br>
        <label class="block font-medium mb-1">Window length</label>
        <input type="number" v-model.number="window.len" min="1" class="w-full border rounded px-2 py-1" />
      </div>
      <div>
        <label class="block font-medium mb-1">Step size</label>
        <input type="number" v-model.number="window.step" min="1" class="w-full border rounded px-2 py-1" />
      </div>
    </div>

    <button
      class="btn btn-primary"
      :disabled="!canWindow || loading"
      @click="runSlidingWindow"
    >
      {{ loading ? 'Computing windows…' : 'Run Sliding-Window Metrics' }}
    </button>

    <!-- Sliding-window metrics plot -->
    <div v-if="windowChartData" class="mt-6">
      <h4 class="font-semibold mb-2">Metrics vs Window Index</h4>
      <canvas ref="winCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import axios from 'axios'
import {
  Chart, Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement, LineController
} from 'chart.js'

// register Chart.js pieces
Chart.register(
  Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement, LineController
)

// simple palette
const COLORS = ['#0099C6', '#DD4477', '#66AA00']

// define props
defineProps({
  datasets: { type: Object, required: true }
})

// selection + raw series
const sel = ref({ ds: '', col: '' })
const fullSeries = ref([])
const fullLabels = ref([])

// trimming state
const trim = ref({ start: 0, end: 0 })
const trimmedData = ref(null)

// sliding-window state
const window = ref({ len: 5, step: 1 })
const windowChartData = ref(null)

const loading = ref(false)

// canvas refs & chart instances
const trimCanvas = ref(null)
const winCanvas = ref(null)
let trimChart = null
let winChart = null

// computed guards
const canTrim = computed(() =>
  sel.value.ds && sel.value.col && fullSeries.value.length &&
  trim.value.start >= 0 &&
  trim.value.end < fullSeries.value.length &&
  trim.value.start < trim.value.end
)
const canWindow = computed(() =>
  trimmedData.value &&
  window.value.len > 0 &&
  window.value.step > 0 &&
  window.value.len <= trimmedData.value.data.length
)

// fetch full series before trimming
async function fetchFullSeries() {
  if (!sel.value.ds || !sel.value.col) return
  loading.value = true
  try {
    const res = await axios.post('/api/series-data', {
      dataset: sel.value.ds,
      column: sel.value.col
    })
    fullLabels.value = res.data.x
    fullSeries.value = res.data.y
    trim.value.end = fullSeries.value.length - 1
  } finally {
    loading.value = false
  }
}

// watch for dataset/column change
watch(() => [sel.value.ds, sel.value.col], fetchFullSeries)

// apply trimming & plot
function applyTrim() {
  const s = trim.value.start
  const e = trim.value.end + 1
  const labels = fullLabels.value.slice(s, e)
  const data = fullSeries.value.slice(s, e)
  trimmedData.value = { labels, data }

  if (trimChart) trimChart.destroy()
  trimChart = new Chart(trimCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: sel.value.col,
        data,
        fill: false,
        borderWidth: 2,
        borderColor: COLORS[0],
        pointBackgroundColor: COLORS[0]
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } }
    }
  })
}

// run sliding-window metrics
async function runSlidingWindow() {
  const { len, step } = window.value
  const dataArr = trimmedData.value.data
  const n = dataArr.length
  const count = Math.floor((n - len) / step) + 1

  const pearsonArr = []
  const spearmanArr = []
  const kendallArr = []
  const winIdx = []

  loading.value = true
  for (let i = 0; i < count; i++) {
    const start = i * step
    const segment = dataArr.slice(start, start + len)
    const base = dataArr.slice(0, len)
    try {
      const res = await axios.post('/api/compare', { seriesA: base, seriesB: segment })
      pearsonArr.push(res.data.pearson_r)
      spearmanArr.push(res.data.spearman_rho)
      kendallArr.push(res.data.kendall_tau)
    } catch {
      pearsonArr.push(null)
      spearmanArr.push(null)
      kendallArr.push(null)
    }
    winIdx.push(i)
  }

  windowChartData.value = {
    labels: winIdx,
    datasets: [
      {
        label: "Pearson's r",
        data: pearsonArr,
        fill: false,
        borderWidth: 2,
        borderColor: COLORS[0],
        pointBackgroundColor: COLORS[0]
      },
      {
        label: "Spearman's ρ",
        data: spearmanArr,
        fill: false,
        borderWidth: 2,
        borderColor: COLORS[1],
        pointBackgroundColor: COLORS[1]
      },
      {
        label: "Kendall's τ",
        data: kendallArr,
        fill: false,
        borderWidth: 2,
        borderColor: COLORS[2],
        pointBackgroundColor: COLORS[2]
      }
    ]
  }

  if (winChart) winChart.destroy()
  winChart = new Chart(winCanvas.value, {
    type: 'line',
    data: windowChartData.value,
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        x: { title: { display: true, text: 'Window Index' } },
        y: { title: { display: true, text: 'Metric Value' } }
      }
    }
  })

  loading.value = false
}

// cleanup
onBeforeUnmount(() => {
  if (trimChart) trimChart.destroy()
  if (winChart) winChart.destroy()
})
</script>


<style scoped>
.btn {
  display: inline-block;
  font-size: 1rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s, opacity 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}


.btn-success {
  background-color: #3b82f6;
  color: white;
}
.btn-success:hover:not(:disabled) {
  background-color: #1D4ED8;
  transform: translateY(-1px);
}
.btn-success:active:not(:disabled) {
  background-color: #1E40AF;
  transform: translateY(0);
}

/* Primary (indigo) */
.btn-primary {
  background-color: #3b82f6; 
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background-color: #1D4ED8;
  transform: translateY(-1px);
}
.btn-primary:active:not(:disabled) {
  background-color: #1E40AF; ;
  transform: translateY(0);
}

/* Disabled state for all .btn */
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
