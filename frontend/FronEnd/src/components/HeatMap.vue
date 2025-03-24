<template>
  <div class="heatmap">
    <h1>Mapa de Calor</h1>
    <div class="video-container">
      <img :src="heatmapFeed" 
           alt="Mapa de Calor em Tempo Real" 
           v-if="heatmapFeed && !error"
           @error="handleImageError" />
      
      <div v-if="loading" class="status-message loading">
        <div class="spinner"></div>
        <p>Carregando mapa de calor...</p>
      </div>
      
      <div v-if="error" class="status-message error">
        <p>⚠️ Erro ao carregar o mapa de calor</p>
        <button @click="retryConnection">Tentar novamente</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue';

export default defineComponent({
  name: 'HeatMap',
  setup() {
    const heatmapFeed = ref('');
    const loading = ref(true);
    const error = ref(false);
    const apiBaseUrl = 'http://localhost:5000'; // Ajuste conforme necessário

    const startStream = () => {
      loading.value = true;
      error.value = false;
      // Usando diretamente o endpoint do heatmap como src da imagem
      heatmapFeed.value = `${apiBaseUrl}/heatmap`;
      loading.value = false;
    };

    const retryConnection = () => {
      error.value = false;
      startStream();
    };

    const handleImageError = () => {
      error.value = true;
      loading.value = false;
    };

    onMounted(() => {
      startStream();
    });

    onUnmounted(() => {
      // Limpeza se necessário
    });

    return {
      heatmapFeed,
      loading,
      error,
      retryConnection,
      handleImageError
    };
  }
});
</script>

<style scoped>
.heatmap {
  text-align: center;
  padding: 20px;
}

.video-container {
  position: relative;
  margin: 20px auto;
  border: 2px solid #ff4500; /* Cor laranja para diferenciar o heatmap */
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
  background-color: #ff4500;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #e03e00;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #ff4500;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>