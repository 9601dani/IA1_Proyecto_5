
import './styles.css';
import { createApp } from 'vue'
import App from './App.vue'
import { loadModelAndTokenizer } from './helpers/modelService';

loadModelAndTokenizer().then(() => {
  createApp(App).mount('#app')
});