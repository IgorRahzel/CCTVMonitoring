<template>
  <div class="spaghetti-view">
    <h1>Diagrama de Espaguete</h1>
    <div class="video-container">
      <img :src="spaghettiFeed" 
           alt="Diagrama de Espaguete em Tempo Real" 
           v-if="!error"
           @error="handleImageError" />
      
      <div v-if="error" class="status-message error">
        <p>⚠️ Erro ao carregar o diagrama</p>
        <button @click="retryConnection">Tentar novamente</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'SpaghettiView',
  setup() {
    const spaghettiFeed = ref('http://localhost:5000/spaghetti_diagram');
    const error = ref(false);

    const handleImageError = () => {
      error.value = true;
    };

    const retryConnection = () => {
      error.value = false;
      // Força o navegador a recarregar a imagem
      spaghettiFeed.value = '';
      setTimeout(() => {
        spaghettiFeed.value = 'http://localhost:5000/spaghetti_diagram';
      }, 100);
    };

    return {
      spaghettiFeed,
      error,
      handleImageError,
      retryConnection
    };
  }
});
</script>

<style scoped>
.spaghetti-view {
  text-align: center;
  padding: 20px;
}

.video-container {
  position: relative;
  margin: 20px auto;
  border: 2px solid #9c27b0; /* Cor roxa para diferenciar o diagrama */
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
  background-color: #9c27b0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #7b1fa2;
}
</style>