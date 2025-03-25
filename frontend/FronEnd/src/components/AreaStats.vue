<template>
  <div class="stats-container">
    <h2>Estatísticas das Áreas</h2>
    
    <div v-if="loading" class="status loading">
      <div class="spinner"></div>
      <span>Carregando dados...</span>
    </div>
    
    <div v-if="error" class="status error">
      {{ error }}
      <button @click="reconnect" class="retry-btn">Tentar novamente</button>
    </div>
    
    <div v-if="!loading && !error && tableData.length === 0" class="status info">
      Nenhum dado disponível no momento
    </div>
    
    <table v-if="tableData.length > 0" class="stats-table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in tableData" :key="index">
          <td v-for="(value, colIndex) in row" :key="colIndex">
            {{ value }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'AreasStats',
  data() {
    return {
      headers: [],
      tableData: [],
      loading: true,
      error: null,
      eventSource: null,
      reconnectAttempts: 0
    }
  },
  mounted() {
    this.connect()
  },
  beforeUnmount() {
    this.closeConnection()
  },
  methods: {
    connect() {
      this.closeConnection()
      this.loading = true
      this.error = null
      
      this.eventSource = new EventSource('http://localhost:5000/areas_stats')
      
      this.eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          
          if (data.error) {
            this.error = data.error
            return
          }
          
          if (data.headers && data.rows) {
            this.headers = data.headers
            this.tableData = data.rows
            this.reconnectAttempts = 0
          }
        } catch (e) {
          console.error('Error parsing data:', e)
          this.error = 'Erro ao processar dados'
        } finally {
          this.loading = false
        }
      }
      
      this.eventSource.onerror = () => {
        this.loading = false
        this.error = 'Erro na conexão com o servidor'
        this.scheduleReconnect()
      }
    },
    
    closeConnection() {
      if (this.eventSource) {
        this.eventSource.close()
        this.eventSource = null
      }
    },
    
    scheduleReconnect() {
      if (this.reconnectAttempts < 5) {
        this.reconnectAttempts++
        const delay = Math.min(1000 * this.reconnectAttempts, 10000)
        setTimeout(() => this.connect(), delay)
      }
    },
    
    reconnect() {
      this.reconnectAttempts = 0
      this.connect()
    }
  }
}
</script>

<style scoped>
.stats-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-table th, .stats-table td {
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  text-align: left;
}

.stats-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  position: sticky;
  top: 0;
}

.stats-table tr:nth-child(even) {
  background-color: #fafafa;
}

.stats-table tr:hover {
  background-color: #f0f0f0;
}

.status {
  padding: 15px;
  margin: 20px 0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.loading {
  background-color: #e3f2fd;
  color: #1565c0;
}

.error {
  background-color: #ffebee;
  color: #c62828;
  flex-direction: column;
}

.info {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(21, 101, 192, 0.2);
  border-radius: 50%;
  border-top-color: #1565c0;
  animation: spin 1s ease-in-out infinite;
}

.retry-btn {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #1565c0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background-color: #0d47a1;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>