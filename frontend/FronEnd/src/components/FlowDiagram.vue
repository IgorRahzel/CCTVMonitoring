<template>
    <div class="flow-diagram">
      <h1>Diagrama de Fluxo</h1>
      <img :src="flowDiagramImage" alt="Diagrama de Fluxo" />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import flowDiagramImage from '@/assets/flow-diagram.png';
  
  export default defineComponent({
    data() {
      return {
        flowDiagramImage,
      };
    },
  });
  </script>
  
  <style scoped>
  .flow-diagram {
    text-align: center;
  }
  img {
    max-width: 100%;
    height: auto;
  }
  </style>
  