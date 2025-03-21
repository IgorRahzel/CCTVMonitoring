<template>
    <div class="people-stats">
      <h1>Estatísticas de Pessoas</h1>
      <ul>
        <li>Total de Pessoas: {{ totalPeople }}</li>
        <li>Pessoas com Cesta: {{ withBasket }}</li>
        <li>Pessoas com Carrinho: {{ withCart }}</li>
      </ul>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    data() {
      return {
        totalPeople: 50,
        withBasket: 20,
        withCart: 15,
      };
    },
  });
  </script>
  
  <style scoped>
  .people-stats {
    text-align: center;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 10px 0;
    font-size: 18px;
  }
  </style>
  