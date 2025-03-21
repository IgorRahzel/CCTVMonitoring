<template>
    <div class="heatmap">
      <h1>Mapa de Calor</h1>
      <img :src="heatmapImage" alt="Mapa de Calor" />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import heatmapImage from '@/assets/heatmap.png'; // Importação estática
  
  export default defineComponent({
    data() {
      return {
        heatmapImage, // Use a variável importada
      };
    },
  });
  </script>
  
  <style scoped>
  .heatmap {
    text-align: center;
  }
  img {
    max-width: 100%;
    height: auto;
  }
  </style>