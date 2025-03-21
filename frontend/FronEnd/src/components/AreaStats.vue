<template>
    <div class="area-stats">
      <h1>Estatísticas de Área</h1>
      <table>
        <thead>
          <tr>
            <th>Área</th>
            <th>Número de Pessoas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(stat, index) in stats" :key="index">
            <td>{{ stat.area }}</td>
            <td>{{ stat.people }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    data() {
      return {
        stats: [
          { area: 'Corredor', people: 10 },
          { area: 'Caixa', people: 5 },
          { area: 'Saída', people: 3 },
        ],
      };
    },
  });
  </script>
  
  <style scoped>
  .area-stats {
    text-align: center;
  }
  table {
    width: 80%;
    margin: auto;
    border-collapse: collapse;
  }
  th, td {
    padding: 10px;
    border: 1px solid #ddd;
  }
  th {
    background-color: #f4f4f4;
  }
  </style>
  