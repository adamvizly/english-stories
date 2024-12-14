<template>
  <div id="app">
    <top-navbar />
    <router-view class="main-content"/>
  </div>
</template>

<script setup>
import TopNavbar from './components/TopNavbar.vue'
</script>

<style>
#app {
  font-family: 'Arial', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  background-color: #f4f4f4;
  min-height: 100vh;
}

.main-content {
  padding-top: 20px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

.nav {
  background: #2c3e50;
  padding: 1rem;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #34495e;
}
</style>
