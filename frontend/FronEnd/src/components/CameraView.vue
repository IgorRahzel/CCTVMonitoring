<template>
  <div class="camera-view">
    <h1>Visualização da Câmera</h1>
    <div class="video-container">
      <img :src="videoFeedUrl" 
           alt="Transmissão ao Vivo" 
           v-if="!error"
           @error="handleImageError" />
      
      <div v-if="error" class="status-message error">
        <p>⚠️ Erro ao carregar a transmissão</p>
        <button @click="retryConnection">Tentar novamente</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'CameraView',
  setup() {
    const videoFeedUrl = ref('http://localhost:5000/video_feed');
    const error = ref(false);

    const handleImageError = () => {
      error.value = true;
    };

    const retryConnection = () => {
      error.value = false;
      // Força o navegador a recarregar a imagem
      videoFeedUrl.value = '';
      setTimeout(() => {
        videoFeedUrl.value = 'http://localhost:5000/video_feed';
      }, 100);
    };

    return {
      videoFeedUrl,
      error,
      handleImageError,
      retryConnection
    };
  }
});
</script>

<style scoped>
.camera-view {
  text-align: center;
  padding: 20px;
}

.video-container {
  position: relative;
  margin: 20px auto;
  border: 2px solid #42b983;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f0f0f0;
  min-height: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-container img {
  max-width: 100%;
  max-height: 80vh;
  display: block;
}

.status-message {
  padding: 20px;
  color: #666;
  position: absolute;
  text-align: center;
}

.status-message.error {
  color: #ff4444;
}

button {
  padding: 8px 16px;
  margin-top: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #369f6b;
}
</style>