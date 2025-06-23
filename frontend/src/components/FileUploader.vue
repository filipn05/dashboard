<template>
  <div>
    <input type="file" @change="onFileChange" />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FileUploader',
  methods: {
    async onFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      const form = new FormData();
      form.append('file', file);

      try {
        const res = await axios.post('/api/datasets', form, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        // res.data will be { id: '...', columns: [...] }
        this.$emit('uploaded', res.data);
      } catch (err) {
        const msg = err.response?.data?.error || err.message;
        alert(`Upload failed: ${msg}`);
      }
    }
  }
};
</script>
