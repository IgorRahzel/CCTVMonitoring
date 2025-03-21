<template>
    <div class="spaghetti">
      <h1>Diagrama de Espaguete</h1>
      <img :src="spaghettiImage" alt="Diagrama de Espaguete" />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import spaghettiImage from '@/assets/spaghetti.png';
  
  export default defineComponent({
    data() {
      return {
        spaghettiImage,
      };
    },
  });
  </script>
  
  <style scoped>
  .spaghetti {
    text-align: center;
  }
  img {
    max-width: 100%;
    height: auto;
  }
  </style>
  