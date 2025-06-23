<template>
  <nav class="navbar">
    <div class="container">
      <a href="#load"     class="nav-item">Load Data</a>
      <a href="#datasets" class="nav-item">Datasets</a>
      <a href="#plot"     class="nav-item">Plotting</a>
      <a href="#pairwise" class="nav-item">Pairwise</a>
      <a href="#trim"     class="nav-item">Trim & Sliding-Window</a>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
.navbar {
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 20;
}
.navbar .container {
  max-width: 1024px;
  margin: auto;
  padding: 0.5rem 1rem;
  display: flex;
  gap: 1rem;
}
.nav-item {
  color: #1f2937;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background 0.2s, color 0.2s;
}
.nav-item:hover {
  background: #f3f4f6;
  color: #111827;
}
.nav-item:active {
  background: #e5e7eb;
}
</style>
