<template>
  <div class="person-details">
    <h2>Detalhes da {{ personName }}</h2>
    <button @click="goBack" class="back-button">Voltar</button>
    
    <div v-if="loading" class="status loading">
      <div class="spinner"></div>
      <span>Carregando dados...</span>
    </div>

    <div v-if="error" class="status error">
      {{ error }}
      <button @click="reconnect" class="retry-btn">Tentar novamente</button>
    </div>

    <div v-if="!loading && !error && (!personData || personData.rows.length === 0)" class="status info">
      Nenhum dado disponível para esta pessoa
    </div>

    <div v-if="personData" class="data-container">
      <h3>Estatísticas por Área:</h3>
      
      <!-- Tabela no topo -->
      <table class="stats-table">
        <thead>
          <tr>
            <th v-for="header in personData.headers" :key="header">{{ formatActionName(header) }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in personData.rows" :key="index">
            <td v-for="(value, colIndex) in row" :key="colIndex">
              {{ colIndex > 0 ? (value ? value + 's' : '0s') : value }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Gráfico 1: Ações por Área -->
      <div v-if="showChart" class="chart-container">
        <h3 class="chart-title">Ações por Área</h3>
        <BarChart 
          :chart-data="chartData" 
          :chart-options="chartOptions" 
          :height="400"
          ref="barChart"
        />
      </div>

      <!-- Gráfico 2: Tempo Total por Ação -->
      <div v-if="showChart" class="chart-container">
        <h3 class="chart-title">Tempo Total por Ação</h3>
        <BarChart 
          :chart-data="actionSumChartData" 
          :chart-options="horizontalBarOptions" 
          :height="400"
        />
      </div>

      <!-- Novo Gráfico 3: Tempo Total por Área -->
      <div v-if="showChart" class="chart-container">
        <h3 class="chart-title">Tempo Total por Área</h3>
        <BarChart 
          :chart-data="areaTimeChartData" 
          :chart-options="areaTimeChartOptions" 
          :height="400"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Chart as ChartJS, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js'
import { BarChart } from 'vue-chart-3'

ChartJS.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'PersonDetails',
  components: { BarChart },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const personId = route.params.id
    const personName = ref(`Pessoa ${personId}`)
    const personData = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const reconnectAttempts = ref(0)
    const barChart = ref(null)
    let eventSource = null

    // Funções auxiliares
    const getColor = (index) => {
      const colors = [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", 
        "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"
      ]
      return colors[index % colors.length]
    }

    const formatActionName = (action) => {
      const names = {
        'TimePerson': 'Pessoa na Área',
        'TimePersonWithShoppinBasket': 'Com Cesto',
        'TimePersonWithShoppinCart': 'Com Carrinho',
        'Número Total de Pessoas': 'Total Pessoas'
      }
      return names[action] || action
    }

    // Computed properties
    const showChart = computed(() => {
      return personData.value?.rows?.length > 0 && chartData.value?.labels?.length > 0
    })

    const chartData = computed(() => {
      if (!personData.value || personData.value.rows.length === 0) {
        return {
          labels: [],
          datasets: []
        }
      }

      const areas = personData.value.rows.map(row => row[0])
      const actions = personData.value.headers
        .slice(1)
        .filter(header => header.startsWith('Time'))

      const datasets = actions.map((action, index) => {
        const actionIndex = personData.value.headers.indexOf(action)
        
        return {
          label: formatActionName(action),
          data: personData.value.rows.map(row => {
            const value = row[actionIndex]
            return value ? parseFloat(value) : 0
          }),
          backgroundColor: getColor(index),
          borderColor: getColor(index),
          borderWidth: 1
        }
      })

      return {
        labels: areas,
        datasets: datasets.filter(d => d.data.length > 0)
      }
    })

    // Opções para o gráfico de ações por área
    const chartOptions = computed(() => ({
      responsive: true,
      plugins: {
        legend: { 
          position: "top",
          labels: { font: { size: 12 } }
        },
        title: { 
          display: true, 
          text: "Ações por Área",
          font: { size: 18, weight: 'bold' },
          color: '#2c3e50',
          padding: { top: 10, bottom: 30 }
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${context.raw} segundos`
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Áreas',
            font: { weight: 'bold', size: 14 },
            color: '#2c3e50'
          }
        },
        y: { 
          beginAtZero: true,
          title: {
            display: true,
            text: 'Tempo (segundos)',
            font: { weight: 'bold', size: 14 },
            color: '#2c3e50'
          },
          ticks: { callback: value => `${value}s` }
        }
      },
      maintainAspectRatio: false
    }))

    // Dados para o gráfico de tempo total por ação
    const actionSumChartData = computed(() => {
      if (!personData.value || personData.value.rows.length === 0) {
        return { labels: [], datasets: [] }
      }

      const actions = personData.value.headers
        .slice(1)
        .filter(header => header.startsWith('Time'))
      
      const actionSums = actions.map(action => {
        const colIndex = personData.value.headers.indexOf(action)
        return personData.value.rows.reduce((sum, row) => sum + (Number(row[colIndex]) || 0), 0)
      })

      return {
        labels: actions.map(action => formatActionName(action)),
        datasets: [{
          label: 'Tempo Total (segundos)',
          data: actionSums,
          backgroundColor: actions.map((_, index) => getColor(index)),
          borderColor: actions.map((_, index) => getColor(index)),
          borderWidth: 1
        }]
      }
    })

    // Opções para o gráfico horizontal de tempo por ação
    const horizontalBarOptions = computed(() => ({
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { 
          display: true,
          text: 'Tempo Total por Ação (segundos)',
          font: { size: 16, weight: 'bold' }
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.raw} segundos`
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Tempo Total (segundos)',
            font: { weight: 'bold' }
          },
          ticks: { callback: value => `${value}s` }
        },
        y: {
          title: {
            display: true,
            text: 'Ações',
            font: { weight: 'bold' }
          }
        }
      },
      maintainAspectRatio: false
    }))

    // Novo: Dados para o gráfico de tempo total por área
    const areaTimeChartData = computed(() => {
      if (!personData.value || personData.value.rows.length === 0) {
        return { labels: [], datasets: [] }
      }

      const areas = personData.value.rows.map(row => row[0])
      const timeColumns = personData.value.headers
        .slice(1)
        .filter(header => header.startsWith('Time'))

      const areaTotals = personData.value.rows.map(row => {
        return timeColumns.reduce((sum, col) => {
          const colIndex = personData.value.headers.indexOf(col)
          return sum + (Number(row[colIndex]) || 0)
        }, 0)
      })

      return {
        labels: areas,
        datasets: [{
          label: 'Tempo Total (segundos)',
          data: areaTotals,
          backgroundColor: areas.map((_, index) => getColor(index)),
          borderColor: areas.map((_, index) => getColor(index)),
          borderWidth: 1
        }]
      }
    })

    // Novo: Opções para o gráfico de tempo total por área
    const areaTimeChartOptions = computed(() => ({
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { 
          display: true,
          text: 'Tempo Total por Área (segundos)',
          font: { size: 16, weight: 'bold' }
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.raw} segundos`
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Tempo Total (segundos)',
            font: { weight: 'bold' }
          },
          ticks: { callback: value => `${value}s` }
        },
        y: {
          title: {
            display: true,
            text: 'Áreas',
            font: { weight: 'bold' }
          }
        }
      },
      maintainAspectRatio: false
    }))

    // Métodos
    const connect = () => {
      closeConnection()
      loading.value = true
      error.value = null

      eventSource = new EventSource(`http://localhost:5000/api/people-csv/person_${personId}.csv`)

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)

          if (data.error) {
            error.value = data.error
            return
          }

          if (data.headers && data.rows) {
            personData.value = data
            reconnectAttempts.value = 0
          }
        } catch (e) {
          console.error("Error parsing data:", e)
          error.value = "Erro ao processar dados"
        } finally {
          loading.value = false
        }
      }

      eventSource.onerror = () => {
        loading.value = false
        error.value = "Erro na conexão com o servidor"
        scheduleReconnect()
      }
    }

    const closeConnection = () => {
      if (eventSource) {
        eventSource.close()
        eventSource = null
      }
    }

    const scheduleReconnect = () => {
      if (reconnectAttempts.value < 5) {
        reconnectAttempts.value++
        const delay = Math.min(1000 * reconnectAttempts.value, 10000)
        setTimeout(() => connect(), delay)
      }
    }

    const reconnect = () => {
      reconnectAttempts.value = 0
      connect()
    }

    const goBack = () => {
      router.push('/people-stats')
    }

    // Debug
    watch(chartData, (newData) => {
      console.log('Dados do gráfico atualizados:', newData)
    }, { deep: true })

    // Hooks de ciclo de vida
    onMounted(() => {
      connect()
    })

    onBeforeUnmount(() => {
      closeConnection()
    })

    return {
      personName,
      personData,
      loading,
      error,
      goBack,
      reconnect,
      showChart,
      chartData,
      chartOptions,
      actionSumChartData,
      horizontalBarOptions,
      areaTimeChartData, // Novo
      areaTimeChartOptions, // Novo
      formatActionName,
      barChart
    }
  }
}
</script>

<style scoped>
.person-details {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.back-button {
  padding: 8px 16px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s;
  align-self: flex-start;
}

.back-button:hover {
  background-color: #0b7dda;
}

.data-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0 0 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
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

.chart-container {
  margin-top: 30px;
  padding: 30px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 550px;
  position: relative;
}

.chart-container + .chart-container {
  margin-top: 40px;
}

.chart-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: bold;
}

h2, h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

h2 {
  text-align: center;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>