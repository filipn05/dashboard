<template>
  <table v-if="metrics" class="mt-4 w-full text-left border-collapse">
    <thead>
      <tr class="bg-gray-100">
        <th class="px-2 py-1 border">Metric</th>
        <th class="px-2 py-1 border">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="px-2 py-1 border">Pearson’s r</td>
        <td class="px-2 py-1 border">{{ metrics.pearson_r.toFixed(4) }}</td>
      </tr>
      <tr>
        <td class="px-2 py-1 border">Spearman’s ρ</td>
        <td class="px-2 py-1 border">{{ metrics.spearman_rho.toFixed(4) }}</td>
      </tr>
      <tr>
        <td class="px-2 py-1 border">Kendall’s τ</td>
        <td class="px-2 py-1 border">{{ metrics.kendall_tau.toFixed(4) }}</td>
      </tr>
      <tr>
        <td class="px-2 py-1 border">MSE</td>
        <td class="px-2 py-1 border">{{ metrics.mse.toFixed(4) }}</td>
      </tr>
      <tr>
        <td class="px-2 py-1 border">DTW distance</td>
        <td class="px-2 py-1 border">{{ metrics.dtw.toFixed(4) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'MetricsTable',
  props: {
    metrics: {
      type: Object,
      required: false,
      default: null
    }
  }
}
</script>

<style scoped>
table th, table td {
  border: 1px solid #ddd;
}
</style>
