<template>
  <div class="home">
    <h1>Bem-vindo ao Sistema de Análise de Vídeo</h1>
    <carousel 
      :items-to-show="3"
      :autoplay="3000"
      :wrap-around="true"
      :transition="500"
    >
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
import 'vue3-carousel/dist/carousel.css';

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
  padding: 20px;
}
.carousel-item {
  padding: 30px;
  border: 1px solid #42b983;
  border-radius: 8px;
  margin: 10px;
  cursor: pointer;
  transition: transform 0.3s;
  background-color: #f8f8f8;
}
.carousel-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.carousel-item h2 {
  color: #2c3e50;
  margin: 0;
}
</style>