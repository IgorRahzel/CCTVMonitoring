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
          <th v-for="header in headers" :key="header">{{ formatActionName(header) }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in tableData" :key="index">
          <td v-for="(value, colIndex) in row" :key="colIndex">
            {{ colIndex > 0 ? (value ? value + 's' : '0s') : value }}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Gráfico de Barras -->
    <div v-if="showChart" class="chart-container">
      <h3 class="chart-title">Ações por Área</h3>
      <BarChart :chart-data="chartData" :chart-options="chartOptions" :height="400" />
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { Chart as ChartJS, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from "chart.js";
import { BarChart } from "vue-chart-3";

// Registrar todos os componentes necessários do Chart.js
ChartJS.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

export default defineComponent({
  name: "AreasStats",
  components: { BarChart },
  data() {
    return {
      headers: [],
      tableData: [],
      loading: true,
      error: null,
      eventSource: null,
      reconnectAttempts: 0
    };
  },
  computed: {
    showChart() {
      return this.tableData.length > 0 && this.chartData?.labels?.length > 0;
    },
    chartData() {
      if (this.tableData.length === 0) return { labels: [], datasets: [] };

      const areas = this.tableData.map(row => row[0]);
      const actions = this.headers.slice(1);
      
      const datasets = actions.map((action, index) => {
        const isTimeColumn = action.startsWith('Time');
        
        return {
          label: this.formatActionName(action),
          data: this.tableData.map(row => {
            const value = row[index + 1];
            const numericValue = value ? Number(value) : 0;
            return isTimeColumn ? numericValue : null;
          }).filter(val => val !== null),
          backgroundColor: this.getColor(index),
          borderColor: this.getColor(index),
          borderWidth: 1
        };
      }).filter(dataset => dataset.data.length > 0);

      return {
        labels: areas,
        datasets
      };
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { 
            position: "top",
            labels: {
              font: {
                size: 12
              }
            }
          },
          title: { 
            display: true, 
            text: "Ações por Área",
            font: {
              size: 18,
              weight: 'bold'
            },
            color: '#2c3e50',
            padding: {
              top: 10,
              bottom: 30
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${context.raw} segundos`;
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Áreas',
              font: {
                weight: 'bold',
                size: 14
              },
              color: '#2c3e50'
            }
          },
          y: { 
            beginAtZero: true,
            title: {
              display: true,
              text: 'Tempo (segundos)',
              font: {
                weight: 'bold',
                size: 14
              },
              color: '#2c3e50'
            },
            ticks: {
              callback: function(value) {
                return value + 's';
              }
            }
          }
        },
        maintainAspectRatio: false
      };
    }
  },
  mounted() {
    this.connect();
  },
  beforeUnmount() {
    this.closeConnection();
  },
  methods: {
    connect() {
      this.closeConnection();
      this.loading = true;
      this.error = null;

      this.eventSource = new EventSource("http://localhost:5000/areas_stats");

      this.eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.error) {
            this.error = data.error;
            return;
          }

          if (data.headers && data.rows) {
            this.headers = data.headers;
            this.tableData = data.rows;
            this.reconnectAttempts = 0;
          }
        } catch (e) {
          console.error("Error parsing data:", e);
          this.error = "Erro ao processar dados";
        } finally {
          this.loading = false;
        }
      };

      this.eventSource.onerror = () => {
        this.loading = false;
        this.error = "Erro na conexão com o servidor";
        this.scheduleReconnect();
      };
    },
    closeConnection() {
      if (this.eventSource) {
        this.eventSource.close();
        this.eventSource = null;
      }
    },
    scheduleReconnect() {
      if (this.reconnectAttempts < 5) {
        this.reconnectAttempts++;
        const delay = Math.min(1000 * this.reconnectAttempts, 10000);
        setTimeout(() => this.connect(), delay);
      }
    },
    reconnect() {
      this.reconnectAttempts = 0;
      this.connect();
    },
    getColor(index) {
      const colors = [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", 
        "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"
      ];
      return colors[index % colors.length];
    },
    formatActionName(action) {
      const names = {
        'TimePerson': 'Pessoa na Área',
        'TimePersonWithShoppinBasket': 'Com Cesto',
        'TimePersonWithShoppinCart': 'Com Carrinho',
        'Número Total de Pessoas': 'Total Pessoas'
      };
      return names[action] || action;
    }
  }
});
</script>

<style scoped>
.stats-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0 40px 0;
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

.chart-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: bold;
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>