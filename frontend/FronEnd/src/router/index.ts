import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/HomeView.vue';
import Heatmap from '@/components/HeatMap.vue';
import Spaghetti from '@/components/Spaghetti.vue';
import FlowDiagram from '@/components/FlowDiagram.vue';
import AreaStats from '@/components/AreaStats.vue';
import PeopleStats from '@/components/PeopleStats.vue';
import CameraView from '@/components/CameraView.vue';
import PersonDetails from '@/components/PersonDetails.vue'; // Importe o novo componente

const routes = [
  { 
    path: '/', 
    component: Home 
  },
  { 
    path: '/heatmap', 
    component: Heatmap 
  },
  { 
    path: '/spaghetti', 
    component: Spaghetti 
  },
  { 
    path: '/flow-diagram', 
    component: FlowDiagram 
  },
  { 
    path: '/area-stats', 
    component: AreaStats 
  },
  { 
    path: '/people-stats', 
    component: PeopleStats 
  },
  { 
    path: '/camera-view', 
    component: CameraView 
  },
  // Adicione a nova rota para detalhes da pessoa
  { 
    path: '/person-details/:id',  // :id é um parâmetro dinâmico
    name: 'PersonDetails',        // Nome da rota para navegação programática
    component: PersonDetails,
    props: true                   // Permite passar o parâmetro como prop
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;