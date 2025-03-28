<template>
  <div class="home">
    <h1>Bem-vindo ao Sistema de Análise de Vídeo</h1>
    <div class="carousel-container">
      <carousel 
        :items-to-show="3"
        :autoplay="3000"
        :wrap-around="true"
        :transition="500"
        :pause-autoplay-on-hover="true"
        ref="myCarousel"
      >
        <template #addons>
          <navigation />
        </template>
        
        <slide v-for="(option, index) in options" :key="index">
          <div class="carousel-item" @click="navigate(option.page)">
            <h2>{{ option.title }}</h2>
          </div>
        </slide>
      </carousel>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { Carousel, Slide, Navigation } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

export default defineComponent({
  components: {
    Carousel,
    Slide,
    Navigation
  },
  setup() {
    const router = useRouter();
    const myCarousel = ref();

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

    return { 
      options, 
      navigate,
      myCarousel
    };
  },
});
</script>

<style scoped>
.home {
  text-align: center;
  padding: 20px;
}

.carousel-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 60px;
  position: relative;
}

.carousel-item {
  padding: 30px;
  border: 1px solid #42b983;
  border-radius: 8px;
  margin: 10px;
  cursor: pointer;
  transition: transform 0.3s;
  background-color: #f8f8f8;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  background-color: #e8f5e9;
}

.carousel-item h2 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.2rem;
}

/* Estilização personalizada para as setas */
:deep(.carousel__prev),
:deep(.carousel__next) {
  background-color: #42b983;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}

:deep(.carousel__prev) {
  left: -50px !important;
}

:deep(.carousel__next) {
  right: -50px !important;
}

:deep(.carousel__prev:hover),
:deep(.carousel__next:hover) {
  background-color: #3aa876;
  transform: scale(1.1);
}

:deep(.carousel__prev--disabled),
:deep(.carousel__next--disabled) {
  opacity: 0.5;
  cursor: not-allowed;
}

:deep(.carousel__icon) {
  width: 20px;
  height: 20px;
}

/* Ajuste para dispositivos móveis */
@media (max-width: 768px) {
  .carousel-container {
    padding: 0 40px;
  }
  
  .carousel-item {
    padding: 20px;
    height: 100px;
  }
  
  .carousel-item h2 {
    font-size: 1rem;
  }
  
  :deep(.carousel__prev),
  :deep(.carousel__next) {
    width: 30px;
    height: 30px;
  }

  :deep(.carousel__prev) {
    left: -30px !important;
  }

  :deep(.carousel__next) {
    right: -30px !important;
  }
}

/* Ajuste para telas muito pequenas */
@media (max-width: 480px) {
  .carousel-container {
    padding: 0 30px;
  }

  :deep(.carousel__prev) {
    left: -20px !important;
  }

  :deep(.carousel__next) {
    right: -20px !important;
  }
}
</style>