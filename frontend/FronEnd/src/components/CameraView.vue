<template>
    <div class="camera-view">
      <h1>Visualização da Câmera</h1>
      <img :src="cameraFeed" alt="Câmera ao Vivo" />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  
  export default defineComponent({
    setup() {
      const cameraFeed = ref('');
  
      const fetchCameraImage = async () => {
        try {
          const response = await fetch('http://localhost:5000/camera'); // Altere para o endpoint correto
          const blob = await response.blob();
          cameraFeed.value = URL.createObjectURL(blob);
        } catch (error) {
          console.error('Erro ao carregar a câmera:', error);
        }
      };
  
      onMounted(() => {
        fetchCameraImage();
        setInterval(fetchCameraImage, 1000); // Atualiza a imagem a cada segundo
      });
  
      return { cameraFeed };
    },
  });
  </script>
  
  <style scoped>
  .camera-view {
    text-align: center;
  }
  img {
    max-width: 100%;
    height: auto;
  }
  </style>
  