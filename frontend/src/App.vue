<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Navbar with inline links -->
    <header class="header">
      <div class="header__inner">
        <h1 class="header__title">Time-Series Dashboard</h1>
        <nav class="header__nav">
          <a href="#load"     class="header__link">Load Data</a>
          <a href="#datasets" class="header__link">Datasets</a>
          <a href="#plot"     class="header__link">Plotting</a>
          <a href="#pairwise" class="header__link">Pairwise</a>
          <a href="#trim"     class="header__link">Trim &amp; Window</a>
        </nav>
      </div>
    </header>

    <!-- Main content -->
    <main class="max-w-6xl mx-auto p-6 space-y-8">

      <!-- Upload panel -->
      <section id="load" class="bg-white p-6 rounded-lg shadow">
        <div class="section-header">Load Data</div>
        <div class="section-body">
          <FileUploader @uploaded="refreshDatasets" />
        </div>
      </section>

      <!-- Dataset list -->
      <section id="datasets" class="bg-white p-6 rounded-lg shadow">
        <div class="section-header">Loaded Datasets</div>
        <div class="section-body">
          <DatasetList :datasets="datasets" @removed="refreshDatasets" />
        </div>
      </section>

      <!-- Plot all / subset panel -->
      <section id="plot" class="bg-white p-6 rounded-lg shadow">
        <div class="section-header">Plotting</div>
        <div class="section-body">
          <PlotPanel :datasets="datasets" />
        </div>
      </section>

      <!-- Pairwise comparison panel -->
      <section id="pairwise" class="bg-white p-6 rounded-lg shadow">
        <div class="section-header">Pairwise Comparison</div>
        <div class="section-body">
          <PairwisePanel :datasets="datasets" />
        </div>
      </section>

      <!-- Trimming & sliding-window analysis panel -->
      <section id="trim" class="bg-white p-6 rounded-lg shadow">
        <div class="section-header">Trim & Sliding-Window Analysis</div>
        <div class="section-body">
          <SlidingWindowPanel :datasets="datasets" />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import FileUploader from './components/FileUploader.vue'
import DatasetList from './components/DatasetList.vue'
import PlotPanel from './components/PlotPanel.vue'
import PairwisePanel from './components/PairwisePanel.vue'
import SlidingWindowPanel from './components/SlidingWindowPanel.vue'
import './assets/dashboard.css'


const datasets = ref({})

async function refreshDatasets() {
  try {
    const res = await axios.get('/api/datasets')
    datasets.value = res.data
  } catch (e) {
    console.error('Failed to fetch datasets', e)
  }
}

onMounted(refreshDatasets)
</script>

<style scoped>
/* Header container */
.header {
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header__inner {
  max-width: 1024px;
  margin: 0 auto;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
/* Title */
.header__title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
}
/* Nav links */
.header__nav {
  display: flex;
  gap: 1rem;
}
.header__link {
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background 0.2s;
}
.header__link:hover {
  background: #f3f4f6;
}
</style>
