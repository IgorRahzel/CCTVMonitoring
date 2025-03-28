<template>
  <div class="people-stats-container">
    <h2>Estatísticas por Pessoa</h2>
    
    <button @click="fetchPeopleList" class="fetch-button">
      {{ loading ? 'Carregando...' : 'Atualizar Lista de Pessoas' }}
    </button>

    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="fetchPeopleList" class="retry-btn">Tentar novamente</button>
    </div>

    <div v-if="peopleList.length > 0" class="people-list">
      <h3>Pessoas Detectadas:</h3>
      <ul>
        <li v-for="person in peopleList" :key="person" @click="viewPersonDetails(person)">
          {{ formatPersonName(person) }}
        </li>
      </ul>
    </div>

    <div v-if="!loading && peopleList.length === 0" class="no-data">
      Nenhuma pessoa detectada ainda
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'PeopleStats',
  setup() {
    const router = useRouter()
    const peopleList = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Conexão SSE para lista de pessoas
    let eventSource

    const connectToSSE = () => {
      if (eventSource) eventSource.close()
      
      eventSource = new EventSource('http://localhost:5000/api/people-csv')
      
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.error) {
          error.value = data.error
        } else {
          peopleList.value = data.files || []
          error.value = null
        }
      }
      
      eventSource.onerror = () => {
        error.value = "Erro na conexão com o servidor"
        // Reconexão automática após 5 segundos
        setTimeout(connectToSSE, 5000)
      }
    }

    const fetchPeopleList = () => {
      loading.value = true
      error.value = null
      connectToSSE()
      loading.value = false
    }

    const formatPersonName = (filename) => {
      // Converte "person_1.csv" para "Pessoa 1"
      return filename.replace('person_', 'Pessoa ').replace('.csv', '')
    }

    const viewPersonDetails = (filename) => {
      const personId = filename.replace('person_', '').replace('.csv', '')
      router.push(`/person-details/${personId}`)
    }

    // Inicia a conexão quando o componente é montado
    fetchPeopleList()

    // Fecha a conexão quando o componente é desmontado
    const cleanup = () => {
      if (eventSource) eventSource.close()
    }

    return {
      peopleList,
      loading,
      error,
      fetchPeopleList,
      formatPersonName,
      viewPersonDetails,
      cleanup
    }
  },
  beforeUnmount() {
    this.cleanup()
  }
}
</script>

<style scoped>
.people-stats-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.fetch-button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}

.fetch-button:hover {
  background-color: #45a049;
}

.people-list {
  margin-top: 20px;
}

.people-list ul {
  list-style-type: none;
  padding: 0;
}

.people-list li {
  padding: 10px;
  margin: 5px 0;
  background-color: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
}

.people-list li:hover {
  background-color: #e0e0e0;
}

.error-message {
  color: #d32f2f;
  background-color: #fde0e0;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.no-data {
  color: #666;
  font-style: italic;
}

.retry-btn {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
</style>