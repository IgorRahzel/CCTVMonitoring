import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importando o Vue Router
import 'vue3-carousel/dist/carousel.css';
//import './assets/styles.css'; // Estilos globais (opcional)

const app = createApp(App);

app.use(router); // Registrando o Vue Router

app.mount('#app'); // Montando a aplicação no elemento root
