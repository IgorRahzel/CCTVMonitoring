<template>
    <div class="person-details">
      <h2>Detalhes da {{ personName }}</h2>
      <button @click="goBack" class="back-button">Voltar</button>
      
      <div v-if="loading" class="loading">Carregando dados...</div>
      
      <div v-if="error" class="error">{{ error }}</div>
      
      <div v-if="personData" class="data-container">
        <h3>Estatísticas por Área:</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in personData.headers" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in personData.rows" :key="index">
              <td v-for="(value, colIndex) in row" :key="colIndex">
                {{ value }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  
  export default {
    name: 'PersonDetails',
    setup() {
      const route = useRoute()
      const router = useRouter()
      const personId = route.params.id
      const personName = ref(`Pessoa ${personId}`)
      const personData = ref(null)
      const loading = ref(false)
      const error = ref(null)
      let eventSource
  
      const fetchPersonData = () => {
        loading.value = true
        error.value = null
        
        eventSource = new EventSource(`http://localhost:5000/api/people-csv/person_${personId}.csv`)
        
        eventSource.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (data.error) {
            error.value = data.error
          } else {
            personData.value = data
            error.value = null
          }
          loading.value = false
        }
        
        eventSource.onerror = () => {
          error.value = "Erro na conexão com os dados da pessoa"
          loading.value = false
        }
      }
  
      const goBack = () => {
        router.push('/people-stats')
      }
  
      onMounted(() => {
        fetchPersonData()
      })
  
      onBeforeUnmount(() => {
        if (eventSource) eventSource.close()
      })
  
      return {
        personName,
        personData,
        loading,
        error,
        goBack
      }
    }
  }
  </script>
  
  <style scoped>
  .person-details {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .back-button {
    padding: 8px 12px;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  .back-button:hover {
    background-color: #0b7dda;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
  }
  
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .loading {
    color: #666;
    font-style: italic;
  }
  
  .error {
    color: #d32f2f;
    background-color: #fde0e0;
    padding: 10px;
    border-radius: 4px;
    margin: 20px 0;
  }
  </style>