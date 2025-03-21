<template>
    <div class="home">
      <h1>Bem-vindo ao Sistema de Análise de Vídeo</h1>
      <carousel :perPage="3" :autoplay=3000 :loop="true">
        <slide v-for="(option, index) in options" :key="index">
          <div class="carousel-item" @click="navigate(option.page)">
            <h2>{{ option.title }}</h2>
          </div>
        </slide>
      </carousel>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useRouter } from 'vue-router';
  import { Carousel, Slide } from 'vue3-carousel';
  
  export default defineComponent({
    components: {
      Carousel,
      Slide,
    },
    setup() {
      const router = useRouter();
  
      const options = [
        { title: 'Mapa de Calor', page: '/heatmap' },
        { title: 'Diagrama de Espaguete', page: '/spaghetti' },
        { title: 'Diagrama de Fluxo', page: '/flow-diagram' },
        { title: 'Estatísticas de Área', page: '/area-stats' },
        { title: 'Estatísticas de Pessoas', page: '/people-stats' },
        { title: 'Visualizar Câmera', page: '/camera-view' },
      ];
  
      const navigate = (page: string) => {
        router.push(page);
      };
  
      return { options, navigate };
    },
  });
  </script>
  
  <style scoped>
  .home {
    text-align: center;
  }
  .carousel-item {
    padding: 20px;
    border: 1px solid #ccc;
    margin: 10px;
    cursor: pointer;
  }
  </style>
  