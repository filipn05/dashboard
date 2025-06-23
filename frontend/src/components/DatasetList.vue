<template>
  <div class="mb-4">
    <h3 class="font-semibold mb-2">Datasets</h3>
    <br>
    <ul v-if="Object.keys(datasets).length">
      <li
        v-for="(meta, id) in datasets"
        :key="id"
        class="flex items-center justify-between py-1"
      >
        <span>{{ meta.name }}</span>
        <button
          class="remove-btn"
          @click="remove(id)"
        >
          Remove
        </button>
      </li>
    </ul>
    <p v-else class="text-gray-500">No datasets uploaded yet.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DatasetList',
  props: {
    datasets: { type: Object, required: true }
  },
  methods: {
    async remove(id) {
      if (!confirm('Delete this dataset?')) return;
      try {
        await axios.delete('/api/datasets', { data: { id } });
        this.$emit('removed', id);
      } catch (err) {
        alert(
          'Failed to remove dataset: ' +
            (err.response?.data?.error || err.message)
        );
      }
    }
  }
};
</script>

<style scoped>
.remove-btn {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  background-color: #ef4444;
  color: #ffffff;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-left: 2rem;   /* <-- push it further away */
}
.remove-btn:hover {
  background-color: #dc2626;
}
</style>
